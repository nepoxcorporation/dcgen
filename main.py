import os
import asyncio
import requests
import zendriver as zd
import random
import string
import json
import re
import socket
import httpx
import base64
import tls_client
import time
import hashlib
import hmac
from datetime import datetime, timezone, timedelta
from dateutil.parser import isoparse
from colorama import Fore, Style, init
from pystyle import Colorate, Colors, Center
import websocket
from tls_client import Session
import warnings
import sys
import logging

warnings.filterwarnings("ignore")
logging.getLogger().setLevel(logging.CRITICAL)

import asyncio
asyncio.get_event_loop().set_exception_handler(lambda loop, context: None)

init(autoreset=True)

sesh = Session(client_identifier="chrome_115", random_tls_extension_order=True)

def send_notification(title, message):
    try:
        notification = Notify()
        notification.application_name = "Electro evs gen"
        notification.title = title
        notification.message = message
        notification.send()
    except Exception as e:
        pass

def log(type, message):
    if type.upper() in ["SUCCESS", "ERROR"]:
        now = datetime.now().strftime("%H:%M:%S")
        type_map = {
            "SUCCESS": Fore.GREEN + "SUCCESS" + Style.RESET_ALL,
            "ERROR": Fore.RED + "ERROR" + Style.RESET_ALL
        }
        tag = type_map.get(type.upper(), type.upper())
        print(f"{Fore.LIGHTBLACK_EX}{now}{Style.RESET_ALL} - {tag} • {message}")

def log(type, message):
    now = datetime.now().strftime("%H:%M:%S")
    type_map = {
        "SUCCESS": Fore.GREEN + "SUCCESS" + Style.RESET_ALL,
        "ERROR": Fore.RED + "ERROR" + Style.RESET_ALL,
        "INFO": Fore.CYAN + "INFO" + Style.RESET_ALL,
        "WARNING": Fore.YELLOW + "WARNING" + Style.RESET_ALL,
        "INPUT": Fore.MAGENTA + "INPUT" + Style.RESET_ALL
    }
    tag = type_map.get(type.upper(), type.upper())

    if type.upper() == "INFO":
        message = f"{Fore.LIGHTBLACK_EX}{message}{Style.RESET_ALL}"
    elif type.upper() == "INPUT":
        pass
    elif ':' in message:
        parts = message.split(':', 1)
        key = parts[0].upper().strip()
        val = parts[1].strip()
        message = f"{key}: {Fore.LIGHTBLACK_EX}{val}{Style.RESET_ALL}"

    print(f"{Fore.LIGHTBLACK_EX}{now}{Style.RESET_ALL} - {tag} • {message}")

def console_title(title="#1 EVS GEN - Electro ^| .gg/furiousmart ^| @g0a4 ^| @electro.me"):
    if os.name == 'nt':
        os.system(f"title {title}")
    else:
        print(f"\33]0;{title}\a", end='', flush=True)

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def cleanup_zendriver():
    try:
        import gc
        gc.collect()
        
        try:
            import zendriver as zd
            zd.stop_all()
        except (ValueError, Exception):
            pass
        
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return
        
        all_tasks = asyncio.all_tasks(loop)
        zendriver_tasks = []
        other_tasks = []
        
        for task in all_tasks:
            if not task.done():
                task_name = str(task)
                if any(keyword in task_name.lower() for keyword in ['listener_loop', 'zendriver', 'websocket', 'connection']):
                    zendriver_tasks.append(task)
                else:
                    other_tasks.append(task)
        
        for task in zendriver_tasks:
            try:
                task.cancel()
            except:
                pass
        
        for task in other_tasks:
            try:
                task.cancel()
            except:
                pass
        
        if zendriver_tasks:
            try:
                done, pending = loop.run_until_complete(
                    asyncio.wait(zendriver_tasks, timeout=1.0, return_when=asyncio.ALL_COMPLETED)
                )
                
                for task in done:
                    try:
                        if not task.cancelled():
                            task.result()
                    except (ValueError, ConnectionError, OSError, asyncio.CancelledError):
                        pass
                    except Exception:
                        pass
                
                for task in pending:
                    try:
                        task.cancel()
                    except:
                        pass
                        
            except (asyncio.TimeoutError, asyncio.CancelledError, RuntimeError):
                pass
            except Exception:
                pass
        
        if other_tasks:
            try:
                done, pending = loop.run_until_complete(
                    asyncio.wait(other_tasks, timeout=0.5, return_when=asyncio.ALL_COMPLETED)
                )
                
                for task in pending:
                    try:
                        task.cancel()
                    except:
                        pass
                        
            except (asyncio.TimeoutError, asyncio.CancelledError, RuntimeError):
                pass
            except Exception:
                pass
        
        gc.collect()
                
    except Exception:
        pass

async def async_cleanup_zendriver():
    try:
        import gc
        gc.collect()
        
        try:
            import zendriver as zd
            zd.stop_all()
        except (ValueError, Exception):
            pass
        
        await asyncio.sleep(0.3)
        
        try:
            loop = asyncio.get_running_loop()
            all_tasks = asyncio.all_tasks(loop)
            
            zendriver_tasks = []
            other_tasks = []
            
            for task in all_tasks:
                if not task.done():
                    task_name = str(task)
                    if any(keyword in task_name.lower() for keyword in ['listener_loop', 'zendriver', 'websocket', 'connection']):
                        zendriver_tasks.append(task)
                    else:
                        other_tasks.append(task)
            
            for task in zendriver_tasks:
                try:
                    task.cancel()
                except:
                    pass
            
            if zendriver_tasks:
                try:
                    done, pending = await asyncio.wait(zendriver_tasks, timeout=1.0, return_when=asyncio.ALL_COMPLETED)
                    
                    for task in done:
                        try:
                            if not task.cancelled():
                                task.result()
                        except (ValueError, ConnectionError, OSError, asyncio.CancelledError):
                            pass
                        except Exception:
                            pass
                    
                    for task in pending:
                        try:
                            task.cancel()
                        except:
                            pass
                except:
                    pass
            
            for task in other_tasks:
                try:
                    task.cancel()
                except:
                    pass
            
            if other_tasks:
                try:
                    await asyncio.wait(other_tasks, timeout=0.2, return_exceptions=True)
                except:
                    pass
                    
        except RuntimeError:
            pass
        
        gc.collect()
                
    except Exception:
        pass

def Slow(text, delay=0.03):
    lines = text.split('\n')
    for line in lines:
        print(line)
        time.sleep(delay)

def vg(lines, start_rgb=(0, 255, 200), end_rgb=(0, 100, 180)):
    total = len(lines)
    result = []
    for i, line in enumerate(lines):
        r = start_rgb[0] + (end_rgb[0] - start_rgb[0]) * i // max(1, total - 1)
        g = start_rgb[1] + (end_rgb[1] - start_rgb[1]) * i // max(1, total - 1)
        b = start_rgb[2] + (end_rgb[2] - start_rgb[2]) * i // max(1, total - 1)
        result.append(f'\033[38;2;{r};{g};{b}m{line}\033[0m')
    return result

def al():
    ascii_art = [
     "███╗░░██╗███████╗██████╗░░█████╗░██╗░░██╗  ██╗░░░██╗██████╗░",
     "████╗░██║██╔════╝██╔══██╗██╔══██╗╚██╗██╔╝  ██║░░░██║╚════██╗",
     "██╔██╗██║█████╗░░██████╔╝██║░░██║░╚███╔╝░  ╚██╗░██╔╝░█████╔╝",
     "██║╚████║██╔══╝░░██╔═══╝░██║░░██║░██╔██╗░  ░╚████╔╝░░╚═══██╗",
     "██║░╚███║███████╗██║░░░░░╚█████╔╝██╔╝╚██╗  ░░╚██╔╝░░██████╔╝",
     "╚═╝░░╚══╝╚══════╝╚═╝░░░░░░╚════╝░╚═╝░░╚═╝  ░░░╚═╝░░░╚═════╝░",

                      "https://mail.proton.me/ UNLIMITED MAIL"
    ]

    print('\n' * 2)
    gradient_lines = vg(ascii_art)
    ascii_text = '\n'.join([Center.XCenter(colored_line) for colored_line in gradient_lines])
    Slow(ascii_text, delay=0.05)
    print('\n' * 2)

def grs(length=10):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def generate_nepox_username():
    """Generate Nepox-related username"""
    prefixes = ["Nepox", "Nepo", "Nep", "Npx", "Nx"]
    suffixes = ["", "User", "Player", "Gamer", "Pro", "Master", "King", "Queen", "Lord", "Gen"]
    numbers = str(random.randint(100, 9999))
    
    prefix = random.choice(prefixes)
    suffix = random.choice(suffixes)
    
    if suffix:
        username = f"{prefix}{suffix}{numbers}"
    else:
        username = f"{prefix}{numbers}"
    
    return username

def generate_nepox_password():
    """Generate Nepox-related password"""
    base_words = ["Nepox", "Nepo", "Nep", "Npx"]
    special_chars = ["!", "@", "#", "$", "%", "&", "*"]
    numbers = str(random.randint(100, 9999))
    
    base = random.choice(base_words)
    special = random.choice(special_chars)
    
    password = f"{base}{numbers}{special}"
    
    # Ensure minimum length of 8 characters
    if len(password) < 8:
        additional_chars = grs(8 - len(password))
        password = f"{base}{numbers}{special}{additional_chars}"
    
    return password

def get_inp(prompt):
    now = datetime.now().strftime("%H:%M:%S")
    input_text = f"{Fore.LIGHTBLACK_EX}{now}{Style.RESET_ALL} - {Fore.MAGENTA}INPUT{Style.RESET_ALL} • {Fore.MAGENTA}{prompt}{Style.RESET_ALL}"
    return input(input_text)

def check_chrome_installation():
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Users\{}\AppData\Local\Google\Chrome\Application\chrome.exe".format(os.getenv('USERNAME', '')),
    ]
    
    for path in chrome_paths:
        if os.path.exists(path):
            return True
    
    log("ERROR", "Chrome not found")
    return False

class BrowserManager:
    def __init__(self):
        self.browser = None

    async def start(self, url):
        self.browser = await zd.start()
        page = await self.browser.get(url)
        await page.wait_for_ready_state('complete', timeout=30000)
        log("SUCCESS", "Registration page opened")
        return page

    async def stop(self):
        if self.browser:
            try:
                await self.browser.stop()
            except Exception as e:
                pass
            finally:
                self.browser = None
            log("SUCCESS", "Browser terminated")

class DiscordFormFiller:
    def __init__(self, email=None, password=None):
        self.browser_mgr = BrowserManager()
        self.password = password
        self.email = email
        self.token = None
        self.credentials_set = False  # Track if credentials have been set

    def get_email_input(self):
        """Get email address from user input"""
        while True:
            email = get_inp("Enter your email address: ").strip()
            if email and '@' in email and '.' in email:
                return email
            else:
                log("ERROR", "Please enter a valid email address")

    def get_password_input(self):
        """Get password from user input or generate Nepox-related one"""
        choice = get_inp("Generate password automatically? (y/n): ").strip().lower()
        if choice in ['y', 'yes']:
            password = generate_nepox_password()
            log("INFO", f"Generated password: {password}")
            return password
        else:
            while True:
                password = get_inp("Enter your password: ").strip()
                if len(password) >= 8:
                    return password
                else:
                    log("ERROR", "Password must be at least 8 characters long")

    def setup_credentials(self):
        """Setup credentials only once to avoid duplicate prompts"""
        if not self.credentials_set:
            # Only ask for email if not provided
            if not self.email:
                self.email = self.get_email_input()
            
            # Always ask for password (or generate)
            if not self.password:
                self.password = self.get_password_input()
            
            self.credentials_set = True
            log("INFO", f"Using email: {self.email}")
            log("INFO", f"Using password: {self.password}")

    async def fill_form(self):
        start_time = time.time()
        try:
            send_notification("Nepox Acc Gen", "Starting account registration...")
            
            # Setup credentials only once (no duplicates)
            self.setup_credentials()
            
            page = await self.browser_mgr.start("https://discord.com/register")

            try:
                await self._fill_basic_fields(page, self.email, self.password)
                log("SUCCESS", "Fields filled!")
                
                await self._select_birth_date(page)
                
                await self._wait_for_captcha_completion(page)
                
                log("INFO", "Registration submitted, waiting for account creation...")
                token = await self._complete_registration()
                
                if token:
                    end_time = time.time()
                    time_taken = end_time - start_time
                    
                    # Final verification check
                    account_info = self.verify_account_status(token)
                    if account_info and account_info.get("verified", False):
                        log("SUCCESS", f"Account fully verified and ready! ({Fore.GREEN}{time_taken:.1f}s{Style.RESET_ALL})")
                    else:
                        log("WARNING", f"Account created but verification pending ({Fore.YELLOW}{time_taken:.1f}s{Style.RESET_ALL})")
                    
                    return token, time_taken
                else:
                    send_notification("Error", "Failed to complete account registration")
                    return None, 0
                
            except Exception as e:
                log("ERROR", f"Form filling failed: {e}")
                try:
                    await self.browser_mgr.stop()
                except Exception as cleanup_error:
                    log("WARNING", f"Browser cleanup failed: {cleanup_error}")
                return None, 0
                
        except Exception as e:
            log("ERROR", f"Account generation failed: {e}")
            try:
                await self.browser_mgr.stop()
            except:
                pass
            return None, 0
            
    async def _countdown_timer(self, duration):
        for i in range(duration):
            remaining = duration - i
            log("INFO", f"Waiting... {remaining}s remaining")
            await asyncio.sleep(1)

    async def _fill_basic_fields(self, page, email, password):
        display_name = "Nepox User"
        username = generate_nepox_username()  # Use Nepox-related username

        email_field = await page.wait_for('input[name="email"]', timeout=15000)
        await email_field.send_keys(email)
        await asyncio.sleep(0.02)

        display_name_field = await page.wait_for('input[name="global_name"]', timeout=15000)
        await display_name_field.send_keys(display_name)
        await asyncio.sleep(0.02)

        username_field = await page.wait_for('input[name="username"]', timeout=15000)
        await username_field.send_keys(username)
        await asyncio.sleep(0.02)

        password_field = await page.wait_for('input[name="password"]', timeout=15000)
        await password_field.send_keys(password)

    async def _select_birth_date(self, page):
        try:
            months = [
                "January", "February", "March", "April", "May", "June",
                "July", "August", "September", "October", "November", "December"
            ]
            random_year = random.randint(1995, 2000)
            random_day = random.randint(1, 28)

            month_attempts = 0
            while month_attempts < 3:
                month_attempts += 1
                random_month = random.choice(months)
                try:
                    month_dropdown = await page.wait_for('div[role="button"][aria-label="Month"]', timeout=15000)
                    await month_dropdown.click()
                    await asyncio.sleep(0.1)

                    month_option = None
                    try:
                        options = await page.query_selector_all('div[role="option"]')
                        if options:
                            month_map = {"january": 0, "february": 1, "march": 2, "april": 3, "may": 4, "june": 5,
                                         "july": 6, "august": 7, "september": 8, "october": 9, "november": 10, "december": 11}
                            month_index = month_map.get(random_month.lower(), 0)
                            if 0 <= month_index < len(options):
                                month_option = options[month_index]
                            if not month_option:
                                for option in options:
                                    try:
                                        text_content = await option.text_content()
                                        if text_content and random_month.lower() in text_content.strip().lower():
                                            month_option = option
                                            break
                                    except:
                                        continue
                    except Exception as e:
                        log("ERROR", f"Error finding month options: {e}")

                    if month_option:
                        await month_option.click()
                        break
                    else:
                        log("WARNING", f"Retrying month")
                        await asyncio.sleep(0.2)
                        continue
                except Exception as e:
                    log("WARNING", f"Month dropdown retry due to error: {e}")
                    await asyncio.sleep(0.2)

            day_attempts = 0
            while day_attempts < 3:
                day_attempts += 1
                try:
                    day_dropdown = await page.wait_for('div[role="button"][aria-label="Day"]', timeout=15000)
                    await day_dropdown.click()
                    await asyncio.sleep(0.1)

                    day_option = None
                    try:
                        options = await page.query_selector_all('div[role="option"]')
                        if options:
                            day_index = min(random_day - 1, len(options) - 1)
                            if 0 <= day_index < len(options):
                                day_option = options[day_index]
                            if not day_option:
                                for option in options:
                                    try:
                                        text_content = await option.text_content()
                                        if text_content and str(random_day) in text_content.strip():
                                            day_option = option
                                            break
                                    except:
                                        continue
                    except Exception as e:
                        log("ERROR", f"Error finding day options: {e}")

                    if day_option:
                        await day_option.click()
                        break
                    else:
                        random_day = random.randint(1, 28)
                        log("WARNING", f"Retrying day")
                        await asyncio.sleep(0.2)
                        continue
                except Exception as e:
                    log("WARNING", f"Day dropdown retry due to error: {e}")
                    await asyncio.sleep(0.2)

            year_attempts = 0
            while year_attempts < 3:
                year_attempts += 1
                try:
                    year_dropdown = await page.wait_for('div[role="button"][aria-label="Year"]', timeout=15000)
                    await year_dropdown.click()
                    await asyncio.sleep(0.1)

                    year_option = None
                    try:
                        options = await page.query_selector_all('div[role="option"]')
                        if options:
                            current_year = 2024
                            year_index = current_year - random_year
                            if 0 <= year_index < len(options):
                                year_option = options[year_index]
                            if not year_option:
                                for option in options:
                                    try:
                                        text_content = await option.text_content()
                                        if text_content and str(random_year) in text_content.strip():
                                            year_option = option
                                            break
                                    except:
                                        continue
                    except Exception as e:
                        log("ERROR", f"Error finding year options: {e}")

                    if year_option:
                        await year_option.click()
                        log("SUCCESS", "Selected Dob")
                        break
                    else:
                        random_year = random.randint(1995, 2002)
                        log("WARNING", f"Retrying year")
                        await asyncio.sleep(0.2)
                        continue
                except Exception as e:
                    log("WARNING", f"Year dropdown retry due to error: {e}")
                    await asyncio.sleep(0.2)

            checkbox = await page.query_selector('input[type="checkbox"]')
            if checkbox:
                await checkbox.click()
                await asyncio.sleep(0.1)

            submit_btn = await page.query_selector('button[type="submit"]')
            if submit_btn:
                await submit_btn.click()
                await asyncio.sleep(1)

        except Exception as e:
            log("ERROR", f"Birth date selection failed: {e}")

    async def _wait_for_captcha_completion(self, page):
        try:
            await asyncio.sleep(0.2)
            
            captcha_detected = False
            for attempt in range(120):
                try:
                    captcha_elements = [
                        'iframe[src*="hcaptcha"]',
                        'iframe[src*="recaptcha"]',
                        'iframe[title*="captcha"]',
                        'iframe[title*="CAPTCHA"]',
                        'div[class*="captcha"]',
                        'div[id*="captcha"]',
                        'div[id*="CAPTCHA"]',
                        '.h-captcha',
                        '.g-recaptcha',
                        '[data-sitekey]'
                    ]
                    
                    captcha_found = False
                    sitekey_value = None
                    for selector in captcha_elements:
                        try:
                            captcha = await page.query_selector(selector)
                            if captcha:
                                is_visible = True
                                try:
                                    is_visible = await captcha.is_visible()
                                except:
                                    pass
                                if is_visible:
                                    captcha_found = True
                                    try:
                                        if selector == '[data-sitekey]':
                                            sitekey_value = await page.evaluate('(el) => el.getAttribute("data-sitekey")', captcha)
                                    except:
                                        pass
                                    break
                        except:
                            continue
                    
                    if captcha_found and not captcha_detected:
                        if sitekey_value:
                            log("INFO", f"Captcha detected (sitekey: {sitekey_value[:10]}...)")
                        else:
                            log("INFO", "Captcha detected")
                        send_notification("Captcha Detected", "Please solve the captcha to continue!")
                        captcha_detected = True
                    
                    if not captcha_found:
                        if captcha_detected:
                            log("SUCCESS", "Captcha solved successfully!")
                            try:
                                await self.browser_mgr.stop()
                            except:
                                pass
                        return True
                    
                    await asyncio.sleep(0.5)
                        
                except Exception:
                    pass
                    
            return True
            
        except Exception as e:
            return True

    def get_token_via_login(self, email, password):
        """Get token by logging in with email and password with better error handling"""
        try:
            payload = {
                'login': email,
                'password': password
            }
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Origin': 'https://discord.com',
                'Referer': 'https://discord.com/login'
            }
            
            response = requests.post('https://discord.com/api/v9/auth/login', 
                                   json=payload, headers=headers, timeout=30)
            
            if response.status_code == 200:
                data = response.json()
                if 'token' in data:
                    return data['token']
                else:
                    log("WARNING", "No token in login response")
                    return None
            elif response.status_code == 400:
                # Invalid credentials or account not ready
                return None
            else:
                log("WARNING", f"Login failed with status: {response.status_code}")
                return None
                
        except requests.exceptions.Timeout:
            log("WARNING", "Login timeout")
            return None
        except Exception as e:
            log("WARNING", f"Token retrieval error: {e}")
            return None

    def verify_account_status(self, token):
        """Verify if account is working and get details with better error handling"""
        url = "https://discord.com/api/v9/users/@me"
        headers = {
            "Authorization": token,
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        try:
            response = requests.get(url, headers=headers, timeout=15)
            if response.status_code == 200:
                data = response.json()
                return {
                    "verified": data.get("verified", False),
                    "email": data.get("email", ""),
                    "username": data.get("username", ""),
                    "discriminator": data.get("discriminator", ""),
                    "id": data.get("id", "")
                }
            elif response.status_code == 401:
                log("WARNING", "Token invalid or expired")
                return None
            else:
                log("WARNING", f"Account API returned status: {response.status_code}")
                return None
        except requests.exceptions.Timeout:
            log("WARNING", "Account verification timeout")
            return None
        except Exception as e:
            log("WARNING", f"Account verification error: {e}")
            return None

    async def _wait_for_account_verification(self, token, max_wait_time=300):
        """Wait for account verification with timeout"""
        start_time = time.time()
        verification_checked = False
        
        while time.time() - start_time < max_wait_time:
            account_info = self.verify_account_status(token)
            
            if account_info:
                if not verification_checked:
                    log("INFO", "Account created successfully, checking verification status...")
                    verification_checked = True
                
                if account_info.get("verified", False):
                    log("SUCCESS", "Account is verified! ✓")
                    return account_info
                else:
                    # Check if we should continue waiting or timeout
                    elapsed = time.time() - start_time
                    remaining = max_wait_time - elapsed
                    
                    if remaining > 60:
                        log("INFO", f"Account not verified yet. Waiting... ({int(remaining)}s remaining)")
                        # Send notification about verification needed
                        send_notification("Verification Required", f"Please verify {self.email} to complete registration")
                    elif remaining > 30:
                        log("WARNING", f"Account still not verified. {int(remaining)}s remaining...")
                    elif remaining > 10:
                        log("WARNING", f"Verification timeout soon: {int(remaining)}s remaining")
                    else:
                        log("WARNING", f"Verification pending - continuing without verification")
                        return account_info
                    
                    await asyncio.sleep(10)  # Check every 10 seconds
            else:
                log("ERROR", "Cannot access account information")
                await asyncio.sleep(5)
        
        # Final check after timeout
        account_info = self.verify_account_status(token)
        if account_info:
            if account_info.get("verified", False):
                log("SUCCESS", "Account verified after waiting! ✓")
            else:
                log("WARNING", "Verification timeout - account created but not verified")
            return account_info
        
        return None

    def _save_account_details(self, email, password, token, account_info):
        """Save account details to saved.txt with verification status"""
        try:
            os.makedirs("output", exist_ok=True)
            with open("output/saved.txt", "a", encoding="utf-8") as f:
                f.write(f"Email: {email}\n")
                f.write(f"Password: {password}\n")
                f.write(f"Token: {token}\n")
                f.write(f"Username: {account_info.get('username', 'N/A')}#{account_info.get('discriminator', '0000')}\n")
                f.write(f"User ID: {account_info.get('id', 'N/A')}\n")
                f.write(f"Verified: {'YES' if account_info.get('verified', False) else 'PENDING'}\n")
                f.write(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write("-" * 50 + "\n")
            
            status = "verified" if account_info.get('verified', False) else "pending verification"
            log("SUCCESS", f"Account details saved to output/saved.txt ({status})")
            
        except Exception as e:
            log("ERROR", f"Failed to save account details: {e}")

    async def _complete_registration(self):
        """Complete the registration process and wait for verification"""
        try:
            log("INFO", "Waiting for registration to complete...")
            
            # Wait for potential email verification or completion
            await asyncio.sleep(5)
            
            # Try to get token via login
            token = None
            max_attempts = 30  # Increased attempts for verification waiting
            for attempt in range(max_attempts):
                token = self.get_token_via_login(self.email, self.password)
                if token:
                    break
                log("INFO", f"Waiting for account to be ready... ({attempt + 1}/{max_attempts})")
                await asyncio.sleep(3)  # Wait longer between attempts
            
            if not token:
                log("ERROR", "Failed to get token after registration - account may not be created")
                return None
            
            # Verify account status and wait for verification if needed
            account_info = await self._wait_for_account_verification(token)
            if account_info:
                token_display = f"{token[:24]}{'*' * 12}"
                log("SUCCESS", f"Token obtained: {token_display}")
                log("INFO", f"Username: {account_info.get('username', 'N/A')}#{account_info.get('discriminator', '0000')}")
                
                if account_info.get("verified", False):
                    log("SUCCESS", "Account verified successfully! ✓")
                else:
                    log("WARNING", "Account verification pending - check your email")
                
                # Save account details
                self._save_account_details(self.email, self.password, token, account_info)
                
                return token
            else:
                log("ERROR", "Failed to verify account status")
                return None
                
        except Exception as e:
            log("ERROR", f"Registration completion failed: {e}")
            return None

async def main():
    clear_screen()
    console_title()

    if not check_chrome_installation():
        log("ERROR", "Chrome not installed")
        log("INFO", "Press Enter to exit...")
        input()
        return

    al()

    try:
        max_runs = int(get_inp("How many accounts to register? (0 = ∞): "))
    except ValueError:
        max_runs = 1

    # Collect emails upfront to avoid duplicate asking
    emails = []
    if max_runs > 0:
        for i in range(max_runs):
            email = get_inp(f"Enter email address for account {i+1}: ").strip()
            while not email or "@" not in email or "." not in email:
                log("ERROR", "Invalid email, try again")
                email = get_inp(f"Enter email address for account {i+1}: ").strip()
            emails.append(email)

    run_count = 0
    total_start_time = time.time()
    successful_accounts = 0

    try:
        while True:
            if max_runs != 0 and run_count >= max_runs:
                break

            # Pick correct email for this account
            email = emails[run_count] if run_count < len(emails) else None
            run_count += 1
            log("SUCCESS", f"Starting account {run_count} registration...")

            try:
                # Each account gets its own filler with email pre-set
                filler = DiscordFormFiller(email=email)
                
                # This will only ask for credentials once (no duplicates)
                result = await filler.fill_form()

                if result and len(result) == 2:
                    token, time_taken = result
                    if token:
                        log("SUCCESS", f"Account registered successfully ({Fore.GREEN}{time_taken:.1f}s{Style.RESET_ALL})")
                        successful_accounts += 1
                    else:
                        log("ERROR", f"Account {run_count} registration failed")
                else:
                    log("ERROR", f"Account {run_count} registration failed")

            except asyncio.CancelledError:
                break
            except Exception as e:
                log("ERROR", f"Account registration error: {e}")
                continue

            if max_runs == 1:
                break
            elif max_runs != 0 and run_count >= max_runs:
                break
            else:
                continue_choice = get_inp("Register another account? (y/n): ").strip().lower()
                if continue_choice not in ['y', 'yes']:
                    break

                
    except KeyboardInterrupt:
        log("SUCCESS", "Exiting...")
    except Exception as e:
        log("ERROR", f"Registration error: {e}")
    finally:
        try:
            await async_cleanup_zendriver()
        except Exception:
            pass
    
    total_end_time = time.time()
    total_time_taken = total_end_time - total_start_time
    log("INFO", f"Registered {successful_accounts} accounts in {Fore.WHITE}({Fore.GREEN}{total_time_taken:.1f}s{Fore.WHITE}){Style.RESET_ALL}")
    
    try:
        await asyncio.sleep(0.5)
    except asyncio.CancelledError:
        pass
    
    try:
        await async_cleanup_zendriver()
    except Exception:
        pass

if __name__ == '__main__':
    import warnings
    warnings.filterwarnings("ignore")
    
    def suppress_exceptions(loop, context):
        exception = context.get('exception')
        if exception and isinstance(exception, (ValueError, ConnectionError, OSError)):
            if 'websocket' in str(exception).lower() or 'connection' in str(exception).lower():
                return
        pass
    
    try:
        if hasattr(asyncio, 'WindowsSelectorEventLoopPolicy'):
            asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.set_exception_handler(suppress_exceptions)
        
        try:
            loop.run_until_complete(main())
        except asyncio.CancelledError:
            pass
        except KeyboardInterrupt:
            log("INFO", "Interrupted by user")
        except Exception as e:
            if not any(keyword in str(e).lower() for keyword in ['websocket', 'connection', 'zendriver']):
                print(f"Error: {e}")
        finally:
            try:
                loop.close()
            except Exception:
                pass
            
    except Exception as e:
        if not any(keyword in str(e).lower() for keyword in ['websocket', 'connection', 'zendriver']):
            print(f"Critical error: {e}")
    finally:
        try:
            cleanup_zendriver()
        except Exception:
            pass
        
        log("INFO", "Press Enter to exit...")
        try:
            input()
        except (KeyboardInterrupt, EOFError):
            pass


