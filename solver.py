#!/usr/bin/env python3
"""
LeetCode Daily Challenge Solver
Automatically solves and submits the daily LeetCode challenge in C++.

Workflow:
1. Manual login (Cloudflare verification + credentials)
2. Fetch daily C++ problem
3. Generate solution with OpenAI GPT-4o
4. Inject code into editor
5. Auto-click Submit button
6. Detect verdict (Accepted/Wrong Answer/etc.)
7. Log results

Usage:
    python3 solver.py
"""

import os
import json
import time
import requests
import re
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # Fallback: parse .env manually
    env_file = Path(".env")
    if env_file.exists():
        with open(env_file) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    os.environ[key.strip()] = value.strip()


class LeetCodeSolver:
    """Solves LeetCode daily challenges in C++ with manual login and automated submission."""

    def __init__(self):
        """Initialize solver with required API keys."""
        self.driver: Optional[webdriver.Chrome] = None
        self.openai_api_key = os.environ.get("OPENAI_API_KEY")

        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY not found in .env file")

    def setup_browser(self) -> None:
        """Initialize Chrome browser for automation."""
        print("🌐 Initializing Chrome browser...")
        options = Options()
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(options=options)
        self.driver.set_page_load_timeout(20)
        print("✓ Browser ready")

    def wait_for_manual_login(self) -> bool:
        """
        Open login page and wait for user to manually authenticate.
        
        This step is necessary because:
        - LeetCode uses Cloudflare bot protection
        - Requires human verification (cannot be automated)
        - Manual login provides authenticated session for API calls
        
        Returns:
            bool: True if login successful, False on timeout
        """
        print("\n" + "=" * 70)
        print("STEP 1: MANUAL LOGIN")
        print("=" * 70)

        self.driver.get("https://leetcode.com/accounts/login/")

        print("""
🔐 A browser has opened to the login page.

INSTRUCTIONS:
  1. Complete Cloudflare verification if prompted
  2. Enter your LeetCode credentials
  3. Click "Sign In"

⏰ Timeout: 3 minutes
The script will continue automatically once logged in.
""")

        try:
            # Wait for redirect away from login page
            WebDriverWait(self.driver, 180).until(
                lambda driver: "login" not in driver.current_url
            )

            time.sleep(2)
            print("✅ Login successful!\n")
            return True

        except Exception as e:
            print(f"\n❌ Login timeout: {e}")
            return False

    def get_daily_challenge(self) -> Dict[str, Any]:
        """
        Fetch the daily coding challenge using GraphQL API.
        
        Uses authenticated session from browser cookies.
        
        Returns:
            dict: Problem data including title, slug, difficulty, content, code snippets
            
        Raises:
            Exception: If GraphQL query fails
        """
        session = requests.Session()

        # Use cookies from authenticated browser session
        for cookie in self.driver.get_cookies():
            session.cookies.set(cookie["name"], cookie["value"])

        query = """
            query activeDailyCodingChallengeQuestion {
                activeDailyCodingChallengeQuestion {
                    question {
                        questionId
                        title
                        titleSlug
                        difficulty
                        content
                        codeSnippets {
                            lang
                            langSlug
                            code
                        }
                    }
                }
            }
        """

        response = session.post("https://leetcode.com/graphql", json={"query": query})
        data = response.json()

        if "errors" in data:
            raise Exception(f"GraphQL error: {data['errors']}")

        return data["data"]["activeDailyCodingChallengeQuestion"]["question"]

    def get_cpp_template(self, code_snippets: list) -> Optional[str]:
        """
        Extract the C++ code template from problem snippets.
        
        Args:
            code_snippets: List of code snippets for different languages
            
        Returns:
            str: C++ template with method signature, or None if not found
        """
        for snippet in code_snippets:
            if snippet["langSlug"] == "cpp":
                return snippet["code"]
        return None

    def generate_solution(
        self, problem: Dict[str, Any], cpp_template: str
    ) -> str:
        """
        Generate C++ solution using OpenAI GPT-4o.
        
        The model receives the problem description and generates code that fills
        the provided method template (respects class structure).
        
        Args:
            problem: Problem data from GraphQL
            cpp_template: The C++ method skeleton to fill
            
        Returns:
            str: Complete C++ code with solution
            
        Raises:
            Exception: If OpenAI API call fails
        """
        # Remove HTML tags from problem content
        content = problem.get("content", "")
        content = re.sub(r"<[^>]+>", "", content)

        title = problem["title"]

        prompt = f"""
You are solving a LeetCode problem in C++.

Problem: {title}
Difficulty: {problem['difficulty']}

Description:
{content}

IMPORTANT CONSTRAINTS:
1. Return ONLY the code that goes INSIDE the method body
2. Do NOT include the method signature or class definition
3. Do NOT include opening {{ or closing }}
4. Code must be valid C++ that compiles
5. Code must solve the problem correctly

Generate the implementation code for the method body. Just the code, no markdown.
"""

        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": f"Bearer {self.openai_api_key}"},
            json={
                "model": "gpt-4o",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3,  # Lower temperature for consistency
            },
            timeout=30,
        )

        response.raise_for_status()
        body = response.json()["choices"][0]["message"]["content"].strip()

        # Remove markdown code blocks if present
        body = re.sub(r"```cpp\n?|\n?```", "", body)
        body = body.strip()

        # Inject solution into template
        full_code = re.sub(
            r"(\{)\s*(\n\s*)(\})",
            rf"\1\n        {body}\n    \3",
            cpp_template,
            count=1,
            flags=re.DOTALL,
        )

        return full_code

    def submit_solution(self, slug: str, code: str) -> Dict[str, Any]:
        """
        Load problem page, inject code, click submit, and wait for verdict.
        
        Args:
            slug: Problem URL slug
            code: Complete C++ solution code
            
        Returns:
            dict: Submission result with status and submitted flag
        """
        print("\n" + "=" * 70)
        print("STEP 2: SUBMISSION")
        print("=" * 70)

        url = f"https://leetcode.com/problems/{slug}/"

        print(f"\n📍 Loading problem page...")
        self.driver.get(url)
        time.sleep(4)

        try:
            # Inject code into editor
            print("💉 Injecting C++ code into editor...")

            # Properly escape code for JavaScript template strings
            escaped_code = code.replace("\\", "\\\\").replace("`", "\\`").replace("$", "\\$")

            js = f"""
            // Try Monaco editor (main LeetCode editor)
            if (window.monaco && window.monaco.editor) {{
                try {{
                    const editors = window.monaco.editor.getEditors();
                    if (editors && editors.length > 0) {{
                        const editor = editors[0];
                        const model = editor.getModel();
                        if (model) {{
                            model.setValue(`{escaped_code}`);
                            editor.focus();
                            return 'monaco';
                        }}
                    }}
                }} catch(e) {{
                    console.log('Monaco error:', e);
                }}
            }}

            // Fallback: Try textarea
            const textarea = document.querySelector('textarea');
            if (textarea) {{
                textarea.value = `{escaped_code}`;
                textarea.dispatchEvent(new Event('change', {{bubbles: true}}));
                textarea.dispatchEvent(new Event('input', {{bubbles: true}}));
                return 'textarea';
            }}

            return 'NOT_FOUND';
            """

            result = self.driver.execute_script(js)
            print(f"✓ Code injected via: {result}")

            if result == "NOT_FOUND":
                print("⚠️  Editor not found, retrying...")
                time.sleep(2)
                result = self.driver.execute_script(js)
                print(f"✓ Retry result: {result}")

            time.sleep(2)

            # Find and click Submit button
            print("\n🔍 Finding Submit button...")
            buttons = self.driver.find_elements(By.TAG_NAME, "button")
            submit_button = None

            for button in buttons:
                if button.text.strip().lower() == "submit":
                    submit_button = button
                    break

            if not submit_button:
                print(f"❌ Submit button not found among {len(buttons)} buttons")
                return {"status": "submit_not_found", "submitted": False}

            # Click submit
            print("⏱️  Clicking Submit button...")
            self.driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
            time.sleep(1)
            submit_button.click()
            print("✓ Submit clicked!")

            time.sleep(2)

            # Wait for verdict
            print("\n⏳ Waiting for verdict...")
            for i in range(120):  # 2 minutes timeout
                page_src = self.driver.page_source

                # Check for verdict keywords
                if "Accepted" in page_src:
                    print("✅ ACCEPTED!")
                    return {"status": "accepted", "submitted": True}
                elif "Wrong Answer" in page_src:
                    print("❌ Wrong Answer")
                    return {"status": "wrong_answer", "submitted": True}
                elif "Compile Error" in page_src:
                    print("❌ Compile Error")
                    return {"status": "compile_error", "submitted": True}
                elif "Runtime Error" in page_src:
                    print("❌ Runtime Error")
                    return {"status": "runtime_error", "submitted": True}
                elif "Time Limit" in page_src:
                    print("⏱️ Time Limit Exceeded")
                    return {"status": "time_limit_exceeded", "submitted": True}
                elif "Memory Limit" in page_src:
                    print("💾 Memory Limit Exceeded")
                    return {"status": "memory_limit_exceeded", "submitted": True}

                time.sleep(1)

                if (i + 1) % 30 == 0:
                    print(f"  Waiting... {i + 1} seconds")

            print("\n⚠️  Verdict not received within 2 minutes")
            return {"status": "timeout", "submitted": True}

        except Exception as e:
            print(f"❌ Error during submission: {e}")
            import traceback
            traceback.print_exc()
            return {"status": "error", "submitted": False}

    def log_result(
        self, problem: Dict[str, Any], code: str, result: Dict[str, Any]
    ) -> None:
        """
        Log submission result to JSON file.
        
        Args:
            problem: Problem data
            code: Generated solution code
            result: Submission result
        """
        log_file = Path("solved_log.json")
        logs = json.loads(log_file.read_text()) if log_file.exists() else []

        logs.append({
            "timestamp": datetime.now().isoformat(),
            "problem_title": problem["title"],
            "problem_slug": problem["titleSlug"],
            "problem_id": problem["questionId"],
            "difficulty": problem["difficulty"],
            "language": "C++",
            "code_length": len(code),
            "result": result,
        })

        log_file.write_text(json.dumps(logs, indent=2))

    def close(self) -> None:
        """Close browser and cleanup resources."""
        if self.driver:
            print("\n🔒 Closing browser...")
            try:
                self.driver.quit()
            except Exception:
                pass


def main():
    """Main entry point."""
    print("\n" + "=" * 70)
    print("LeetCode Daily Challenge Solver")
    print("=" * 70)

    solver = None

    try:
        solver = LeetCodeSolver()
        solver.setup_browser()

        # Step 1: Manual login
        if not solver.wait_for_manual_login():
            return 1

        # Step 2: Fetch daily problem
        print("📝 Fetching daily challenge...")
        problem = solver.get_daily_challenge()
        print(f"✓ Problem: {problem['title']} ({problem['difficulty']})")
        print(f"✓ URL: https://leetcode.com/problems/{problem['titleSlug']}/")

        # Step 3: Get C++ template
        print("\n🔍 Extracting C++ template...")
        cpp_template = solver.get_cpp_template(problem["codeSnippets"])
        if not cpp_template:
            print("❌ C++ template not found")
            return 1
        print("✓ Template found")

        # Step 4: Generate solution
        print("\n🤖 Generating solution with OpenAI GPT-4o...")
        solution = solver.generate_solution(problem, cpp_template)
        print(f"✓ Generated: {len(solution)} characters")

        # Step 5: Submit
        result = solver.submit_solution(problem["titleSlug"], solution)

        if result is None or not result.get("submitted"):
            print("\n❌ Submission failed")
            return 1

        # Log result
        solver.log_result(problem, solution, result)

        # Summary
        print("\n" + "=" * 70)
        print("SUMMARY")
        print("=" * 70)
        print(f"Problem: {problem['title']}")
        print(f"Difficulty: {problem['difficulty']}")
        print(f"Language: C++")
        print(f"Status: {result['status'].upper()}")
        print(f"Code Length: {len(solution)} characters")
        print(f"Logged to: solved_log.json")
        print("=" * 70 + "\n")

        return 0

    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1

    finally:
        if solver:
            solver.close()


if __name__ == "__main__":
    exit(main())
