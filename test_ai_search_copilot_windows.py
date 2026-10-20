import contextlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

import ai_search_copilot_windows as demo
from ai_search_copilot_windows import GRAPH, SCOPES, ask_copilot, build_payload, extract_answer, load_config, main, post_json, sign_in
from read_document import make_chunks, retrieve, tokens

URL = "https://contoso.sharepoint.com/sites/Demo/DNC.txt"
DOCUMENT = Path(__file__).with_name("Ticket_DNC_DEMO.txt").read_text(encoding="utf-8-sig")


class CopilotTests(unittest.TestCase):
    def check_sign_in(self, accounts, silent_result, interactive_result):
        msal_stub = Mock()
        extensions_stub = Mock()
        extensions_stub.build_encrypted_persistence.return_value.is_encrypted = True
        app = msal_stub.PublicClientApplication.return_value
        app.get_accounts.return_value = accounts
        app.acquire_token_silent.return_value = silent_result
        app.acquire_token_interactive.return_value = interactive_result
        with tempfile.TemporaryDirectory() as directory, \
             patch("ai_search_copilot_windows.sys.platform", "win32"), \
             patch.dict("os.environ", {"LOCALAPPDATA": directory}), \
             patch.dict("sys.modules", {"msal": msal_stub, "msal_extensions": extensions_stub}), \
             contextlib.redirect_stdout(io.StringIO()):
            token = sign_in("tenant", "client")
            self.assertIn("token_cache", msal_stub.PublicClientApplication.call_args.kwargs)
            saved_path = Path(extensions_stub.build_encrypted_persistence.call_args.args[0])
            self.assertEqual(saved_path.parent, Path(directory) / "DNC-Copilot-Demo")
            app.initiate_device_flow.assert_not_called()
            return token, app

    def test_cached_login_skips_browser(self):
        token, app = self.check_sign_in([{"id": "one"}], {"access_token": "cached"}, None)
        self.assertEqual(token, "cached")
        app.acquire_token_interactive.assert_not_called()

    def test_expired_cache_opens_browser(self):
        token, app = self.check_sign_in([{"id": "one"}], None, {"access_token": "new"})
        self.assertEqual(token, "new")
        app.acquire_token_interactive.assert_called_once_with(scopes=SCOPES, prompt="select_account", timeout=180)

    def test_first_login_and_multiple_accounts_use_picker(self):
        for accounts in ([], [{"id": "one"}, {"id": "two"}]):
            with self.subTest(accounts=accounts):
                _, app = self.check_sign_in(accounts, None, {"access_token": "new"})
                app.acquire_token_silent.assert_not_called()
                app.acquire_token_interactive.assert_called_once()

    def test_failed_encryption_stops_before_auth(self):
        msal_stub = Mock()
        extensions_stub = Mock()
        extensions_stub.build_encrypted_persistence.return_value.is_encrypted = False
        with tempfile.TemporaryDirectory() as directory, \
             patch("ai_search_copilot_windows.sys.platform", "win32"), \
             patch.dict("os.environ", {"LOCALAPPDATA": directory}), \
             patch.dict("sys.modules", {"msal": msal_stub, "msal_extensions": extensions_stub}):
            with self.assertRaisesRegex(RuntimeError, "không ghi token dạng rõ"):
                sign_in("tenant", "client")
            msal_stub.PublicClientApplication.assert_not_called()

    def test_login_error_explains_redirect_setup(self):
        with self.assertRaisesRegex(RuntimeError, "http://localhost"):
            self.check_sign_in([], None, {"error": "invalid_request"})

    def test_login_error_includes_diagnostics_without_dumping_tokens(self):
        with self.assertRaises(RuntimeError) as raised:
            self.check_sign_in([], None, {
                "error": "invalid_request",
                "error_description": "AADSTS50011: redirect mismatch",
                "error_codes": [50011],
                "correlation_id": "test-correlation",
                "refresh_token": "secret-not-for-output",
            })
        message = str(raised.exception)
        self.assertIn("AADSTS50011", message)
        self.assertIn("test-correlation", message)
        self.assertNotIn("secret-not-for-output", message)

    def test_non_windows_login_is_rejected(self):
        with patch("ai_search_copilot_windows.sys.platform", "linux"):
            with self.assertRaisesRegex(RuntimeError, "Windows DPAPI"):
                sign_in("tenant", "client")

    def test_config_supports_windows_utf8_bom(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "config.json"
            expected = {"tenant_id": "tenant", "client_id": "client", "file_urls": [URL]}
            path.write_text(json.dumps(expected), encoding="utf-8-sig")
            self.assertEqual(load_config(path), expected)

    def test_all_documented_scopes_present(self):
        self.assertEqual(len(SCOPES), 7)
        self.assertIn("https://graph.microsoft.com/ExternalItem.Read.All", SCOPES)

    def test_non_json_http_error_is_readable(self):
        response = Mock(ok=False, status_code=504)
        response.json.side_effect = ValueError("not JSON")
        session = Mock()
        session.post.return_value = response
        with self.assertRaisesRegex(RuntimeError, "HTTP 504"):
            post_json(session, GRAPH, {})

    def test_extracts_final_reply_and_real_citations_only(self):
        citation = {"attributionType": "citation", "seeMoreWebUrl": URL}
        conversation = {"messages": [{"text": "question"}, {"text": "2 khách", "attributions": [citation, {"attributionType": "annotation"}]}]}
        self.assertEqual(extract_answer(conversation, "question"), ("2 khách", [citation]))

    def test_missing_reply_is_not_reported_as_answer(self):
        for result in [{}, {"messages": [{"text": "question"}]}]:
            with self.subTest(result=result), self.assertRaises(RuntimeError):
                extract_answer(result, "question")

    def run_main(self, directory, arguments):
        output, errors = io.StringIO(), io.StringIO()
        with patch.object(demo, "__file__", str(Path(directory) / "ai_search_copilot_windows.py")), \
             patch("sys.argv", ["demo", *arguments]), \
             contextlib.redirect_stdout(output), contextlib.redirect_stderr(errors):
            code = main()
        return code, output.getvalue(), errors.getvalue()

    def prepare_project(self, directory, client_id="04b07795-8ddb-461a-bbee-02f9e1bf7b46"):
        folder = Path(directory)
        (folder / "Ticket_DNC_DEMO.txt").write_text(DOCUMENT, encoding="utf-8")
        (folder / "config.json").write_text(json.dumps({"tenant_id": "test-tenant", "client_id": client_id, "document_path": "Ticket_DNC_DEMO.txt", "file_urls": []}), encoding="utf-8")

    def test_local_retrieval_definitions_and_pending_rules(self):
        chunks = make_chunks(DOCUMENT)
        self.assertEqual(len(chunks), 6)
        self.assertEqual(tokens("ĐỊNH NGHĨA"), tokens("dinh nghia"))
        matches = retrieve("DNC_CALLS khác DNC_CUSTOMERS thế nào?", chunks)
        self.assertEqual({chunk["id"] for _, chunk in matches}, {"S2", "S3"})
        matches = retrieve("Application sau DNC có bắt buộc cùng Ops không?", chunks)
        self.assertEqual(matches[0][1]["id"], "S5")
        self.assertIn("CHƯA XÁC NHẬN", matches[0][1]["text"])

    def test_api_payload_contains_local_excerpts_without_sharepoint_urls(self):
        matches = retrieve("DNC_CALLS DNC_CUSTOMERS", make_chunks(DOCUMENT))
        payload = build_payload("DNC_CALLS DNC_CUSTOMERS", matches, "Ticket_DNC_DEMO.txt")
        self.assertEqual(len(payload["additionalContext"]), 2)
        self.assertIn("[S2]", payload["additionalContext"][0]["text"])
        self.assertNotIn("files", payload["contextualResources"])
        self.assertFalse(payload["contextualResources"]["webContext"]["isWebEnabled"])
        with self.assertRaises(ValueError):
            build_payload("DNC?", [], "demo.txt")

    def test_default_mode_works_with_existing_azure_cli_config_without_login(self):
        with tempfile.TemporaryDirectory() as directory:
            self.prepare_project(directory)
            with patch.object(demo, "sign_in") as login:
                code, output, errors = self.run_main(directory, ["--question", "DNC_CALLS khác DNC_CUSTOMERS thế nào?"])
            self.assertEqual(code, 0, errors)
            login.assert_not_called()
            self.assertIn("[R] RETRIEVAL", output)
            self.assertIn("[A] AUGMENTATION", output)
            self.assertIn("chưa gọi LLM", output)
            prompt = (Path(directory) / "prompt_copilot.txt").read_text(encoding="utf-8-sig")
            self.assertIn("[S2]", prompt)
            self.assertIn("DNC_CALLS = 3", prompt)

    def test_default_mode_does_not_need_config(self):
        with tempfile.TemporaryDirectory() as directory:
            self.prepare_project(directory)
            (Path(directory) / "config.json").unlink()
            code, _, errors = self.run_main(directory, ["--question", "DNC_CALLS DNC_CUSTOMERS"])
            self.assertEqual(code, 0, errors)

    def test_no_hits_clear_previous_prompt_and_never_call_llm(self):
        with tempfile.TemporaryDirectory() as directory:
            self.prepare_project(directory)
            prompt = Path(directory) / "prompt_copilot.txt"
            prompt.write_text("STALE CONTEXT", encoding="utf-8")
            with patch.object(demo, "sign_in") as login, patch.object(demo, "ask_copilot") as ask:
                code, output, _ = self.run_main(directory, ["--question", "Bitcoin Ethereum", "--copilot"])
            self.assertEqual(code, 0)
            login.assert_not_called()
            ask.assert_not_called()
            self.assertIn("CHUA_DU_NGUON", output)
            self.assertNotIn("STALE CONTEXT", prompt.read_text(encoding="utf-8-sig"))

    def test_azure_cli_id_is_blocked_before_auth_but_keeps_ready_prompt(self):
        with tempfile.TemporaryDirectory() as directory:
            self.prepare_project(directory)
            with patch.object(demo, "sign_in") as login:
                code, _, errors = self.run_main(directory, ["--question", "DNC_CALLS DNC_CUSTOMERS", "--copilot"])
            self.assertEqual(code, 1)
            self.assertIn("AADSTS65002", errors)
            self.assertTrue((Path(directory) / "prompt_copilot.txt").is_file())
            login.assert_not_called()

    def test_automatic_mode_passes_retrieved_context_to_real_api_flow_with_mocks(self):
        session = Mock()
        session.__enter__ = Mock(return_value=session)
        session.__exit__ = Mock(return_value=False)
        created = Mock(ok=True)
        created.json.return_value = {"id": "test-conversation"}
        replied = Mock(ok=True)
        replied.json.return_value = {"messages": [{"text": "MOCK ANSWER [S2]"}]}
        session.post.side_effect = [created, replied]
        requests_stub = Mock()
        requests_stub.Session.return_value = session
        with tempfile.TemporaryDirectory() as directory:
            self.prepare_project(directory, client_id="00000000-0000-0000-0000-000000000001")
            with patch.dict("sys.modules", {"requests": requests_stub}), patch.object(demo, "sign_in", return_value="fake-token"):
                code, output, errors = self.run_main(directory, ["--question", "DNC_CALLS DNC_CUSTOMERS", "--copilot"])
            self.assertEqual(code, 0, errors)
            self.assertIn("MOCK ANSWER [S2]", output)
            self.assertEqual(session.post.call_count, 2)
            self.assertEqual(session.post.call_args_list[0].args[0], GRAPH)
            self.assertEqual(session.post.call_args_list[1].args[0], GRAPH + "/test-conversation/chat")
            self.assertIn("additionalContext", session.post.call_args_list[1].kwargs["json"])

    def test_dry_run_prevents_llm_even_when_copilot_flag_is_set(self):
        with tempfile.TemporaryDirectory() as directory:
            self.prepare_project(directory)
            with patch.object(demo, "sign_in") as login:
                code, output, errors = self.run_main(directory, ["--question", "DNC_CALLS DNC_CUSTOMERS", "--copilot", "--dry-run"])
            self.assertEqual(code, 0, errors)
            self.assertIn('"additionalContext"', output)
            login.assert_not_called()

    def test_config_rejects_invalid_document_path_and_missing_source_is_readable(self):
        with tempfile.TemporaryDirectory() as directory:
            folder = Path(directory)
            config = folder / "config.json"
            config.write_text('{"document_path": []}', encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "document_path"):
                load_config(config)
            config.unlink()
            code, _, errors = self.run_main(directory, ["--question", "DNC?"])
            self.assertEqual(code, 1)
            self.assertIn("Ticket_DNC_DEMO.txt", errors)


if __name__ == "__main__":
    unittest.main()
