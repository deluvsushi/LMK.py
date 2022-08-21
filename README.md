# lmk.py
Mobile-API for [LMK](https://play.google.com/store/apps/details?id=com.lightspace.lmk) social network

## Example
```python
import lmk
lmk = lmk.LMKChat()
lmk.request_verification_code(country_code="", phone_number="")
lmk.login(country_code="", phone_number="", verification_code="")
# or
lmk.login_with_access_token(access_token="", device_id="")
```
