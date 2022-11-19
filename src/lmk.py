import requests
from random import sample
from datetime import datetime

class LMK:
	def __init__(self, locale: str = "en_US") -> None:
		self.api = "https://api.lmk.chat"
		self.locale = locale
		self.device_id = self.generate_device_id()
		self.headers = {
			"user-agent": "okhttp/4.8.0",
			"x-deviceid": self.device_id,
			"x-lmk-app-id": "888888",
			"x-lmk-app-locale": self.locale,
			"x-lmk-app-version": "android2.53",
			"x-lmk-carrier-name": "Mobile+TeleSystems"
		}
		self.user_id = None
		self.access_token = None

	def get_current_time(self) -> str:
		return datetime.today().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "+08:00"

	def sign_request(self) -> None:
		self.headers["current_datetime"] = datetime.today().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3] + " +08:00"

	def generate_device_id(self) -> str:
		return "".join(sample("abcdefghijklmnopqrstuvwxyz" + "0123456789", 16))

	def request_verification_code(
			self,
			country_code: int,
			phone_number: int) -> int:
		return requests.get(
			f"{self.api}/verification-tokens?countryCode={country_code}&phoneNumber={phone_number}",
			headers=self.headers).status_code

	def login(
			self,
			country_code: int,
			phone_number: int,
			verification_code: int) -> dict:
		data = {
			"acquisitionChannel": "Null",
			"eventTime": self.get_current_time(),
			"phone": {
				"countryCode": country_code,
				"number": phone_number,
				"verificationCode": verification_code
			},
			"provider": "phone"
		}
		self.sign_request()
		response = requests.post(
			f"{self.api}/authentication?provider=phone",
			json=data,
			headers=self.headers).json()
		if "id" in response:
			self.user_id = response["id"]
			self.access_token = response["session"]["accessToken"]
			self.headers["authorization"] = f"Bearer {self.access_token}"
		return response

	def login_with_access_token(self, access_token: str, device_id: str) -> dict:
		self.device_id = device_id
		self.access_token = access_token
		self.headers["x-deviceid"] = self.device_id
		self.headers["authorization"] = f"Bearer {self.access_token}"
		response = self.get_current_user()
		if "id" in response:
			self.user_id = response["id"]
		return response

	def get_current_user(self, with_extra: bool = True) -> dict:
		return requests.get(
			f"{self.api}/user?withExtra={with_extra}",
			headers=self.headers).json()

	def get_wallet(self) -> dict:
		return requests.get(
			f"{self.api}/user/wallet",
			headers=self.headers).json()

	def get_user_match(self, user_id: str) -> dict:
		return requests.get(
			f"{self.api}/users/{user_id}/match",
			headers=self.headers).json()

	def get_badge_counts(self) -> dict:
		return requests.get(
			f"{self.api}/user/badge-counts",
			headers=self.headers).json()

	def get_restriction(self) -> dict:
		return requests.get(
			f"{self.api}/user/restriction",
			headers=self.headers).json()

	def get_interests(self) -> dict:
		return requests.get(
			f"{self.api}/interests/v2",
			headers=self.headers).json()

	def get_user_info(
			self,
			user_id: str,
			track_view: bool = False) -> dict:
		return requests.get(
			f"{self.api}/users/{user_id}?trackView={track_view}",
			headers=self.headers).json()

	def get_all_rooms(
			self,
			action: str = "Pull_Down_To_Refresh",
			mini_on_boarding: bool = True) -> dict:
		return requests.get(
			f"{self.api}/mario/audio-room/recommendation-rooms?action={action}&miniOnBoarding={mini_on_boarding}",
			headers=self.headers).json()

	def get_following_rooms(self, offset: int = 0, limit: int = 10) -> dict:
		return requests.get(
			f"{self.api}/mario/audio-room/followee-rooms?offset={offset}&limit={limit}",
			headers=self.headers).json()

	def get_interests_rooms(
			self,
			action: str = "Pull_Down_To_Refresh",
			mini_on_boarding: bool = True) -> dict:
		return requests.get(
			f"{self.api}/mario/audio-room/recommendation-rooms?category=Interests&action={action}&miniOnBoarding={mini_on_boarding}",
			headers=self.headers).json()

	def get_discussion_rooms(
			self,
			action: str = "Pull_Down_To_Refresh",
			mini_on_boarding: bool = True) -> dict:
		return requests.get(
			f"{self.api}/mario/audio-room/recommendation-rooms?category=Discussion&action={action}&miniOnBoarding={mini_on_boarding}",
			headers=self.headers).json()

	def get_music_rooms(
			self,
			action: str = "Pull_Down_To_Refresh",
			mini_on_boarding: bool = True) -> dict:
		return requests.get(
			f"{self.api}/mario/audio-room/recommendation-rooms?category=Music&action={action}&miniOnBoarding={mini_on_boarding}",
			headers=self.headers).json()

	def get_gaming_rooms(
			self,
			action: str = "Pull_Down_To_Refresh",
			mini_on_boarding: bool = True) -> dict:
		return requests.get(
			f"{self.api}/mario/audio-room/recommendation-rooms?category=Gaming&action={action}&miniOnBoarding={mini_on_boarding}",
			headers=self.headers).json()

	def get_motivational_rooms(
			self,
			action: str = "Pull_Down_To_Refresh",
			mini_on_boarding: bool = True) -> dict:
		return requests.get(
			f"{self.api}/mario/audio-room/recommendation-rooms?category=Motivational&action={action}&miniOnBoarding={mini_on_boarding}",
			headers=self.headers).json()

	def get_casual_rooms(
			self,
			action: str = "Pull_Down_To_Refresh",
			mini_on_boarding: bool = True) -> dict:
		return requests.get(
			f"{self.api}/mario/audio-room/recommendation-rooms?category=Casual&action={action}&miniOnBoarding={mini_on_boarding}",
			headers=self.headers).json()

	def get_relationships_rooms(
			self,
			action: str = "Pull_Down_To_Refresh",
			mini_on_boarding: bool = True) -> dict:
		return requests.get(
			f"{self.api}/mario/audio-room/recommendation-rooms?category=Relationships&action={action}&miniOnBoarding={mini_on_boarding}",
			headers=self.headers).json()

	def search_audio_room(self, search_key: str) -> dict:
		return requests.get(
			f"{self.api}/mario/audio-room/room?searchKey={search_key}",
			headers=self.headers).json()

	def join_room(
			self,
			room_id: str,
			impression_id: str,
			origin: int = 303) -> dict:
		return requests.get(
			f"{self.api}/mario/audio-room/join-room?roomId={room_id}&impressionId={impression_id}&origin={origin}",
			headers=self.headers).json()

	def get_room_last_messages(self, room_id: str) -> dict:
		return requests.get(
			f"{self.api}/mario/audio-room/rooms/{room_id}/last-messages",
			headers=self.headers).json()

	def get_room_video(self, room_id: str) -> dict:
		return requests.get(
			f"{self.api}/mario/audio-room/rooms/{room_id}/video",
			headers=self.headers).json()

	def get_room_boost(self, room_id: str) -> dict:
		return requests.get(
			f"{self.api}/mario/audio-room/rooms/{room_id}/boost",
			headers=self.headers).json()

	def get_user_followings(
			self,
			user_id: str,
			page: int = 0,
			limit: int = 10) -> dict:
		return requests.get(
			f"{self.api}/users/{user_id}/following?page={page}&limit={limit}",
			headers=self.headers).json()

	def get_user_followers(
			self,
			user_id: str,
			page: int = 0,
			limit: int = 10) -> dict:
		return requests.get(
			f"{self.api}/users/{user_id}/followers?page={page}&limit={limit}",
			headers=self.headers).json()

	def get_profile_visitors(self) -> dict:
		return requests.get(
			f"{self.api}/user/visitors",
			headers=self.headers).json()

	def get_received_gifts(self, page: int = 0, limit: int = 20) -> dict:
		return requests.get(
			f"{self.api}/mario/audio-room/user/received-gifts?page={page}&limit={limit}",
			headers=self.headers).json()

	def get_sent_gifts(self, page: int = 0, limit: int = 20) -> dict:
		return requests.get(
			f"{self.api}/mario/audio-room/user/sent-gifts?page={page}&limit={limit}",
			headers=self.headers).json()

	def get_journey(self) -> dict:
		return requests.get(
			f"{self.api}/user/journey",
			headers=self.headers).json()

	def claim_journey(self, journey_number: int = 0) -> dict:
		data = {
			"journey": journey_number
		}
		return requests.post(
			f"{self.api}/user/journey:markCompleted",
			json=data,
			headers=self.headers).json()

	def redeem_code(self, code: str) -> dict:
		data = {
			"invitationCode": code
		}
		return requests.post(
			f"{self.api}/influencer/invitation-rewards",
			json=data,
			headers=self.headers).json()

	def get_store_gem_packets(self) -> dict:
		return requests.get(
			f"{self.api}/store/gemPackets/v2",
			headers=self.headers).json()

	def get_wallet_transactions(
			self,
			page: int = 0,
			limit: int = 20) -> dict:
		return requests.get(
			f"{self.api}/user/walletTransactions?page={page}&limit={limit}",
			headers=self.headers).json()

	def follow_user(
			self,
			user_id: str,
			origin: str = "profile_followUser_onProfilePage") -> dict:
		data = {
			"followeeId": user_id,
			"origin": origin
		}
		return requests.post(
			f"{self.api}/users/{self.user_id}/following",
			json=data,
			headers=self.headers).status_code

	def unfollow_user(self, user_id: str) -> dict:
		return requests.delete(
			f"{self.api}/users/{self.user_id}/following/{user_id}",
			headers=self.headers).status_code

	def edit_profile(
			self,
			profile_message: str = None,
			first_name: str = None,
			gender: str = None,
			job: str = None,
			company: str = None,
			school: str = None) -> dict:
		data = {}
		if profile_message:
			data["profileMessage"] = profile_message
		if first_name:
			data["firstName"] = first_name
		if gender:
			data["gender"] = gender
		if job:
			data["job"] = job
		if company:
			data["company"] = company
		if school:
			data["school"] = school
		return requests.put(
			f"{self.api}/user",
			json=data,
			headers=self.headers).json()

	def get_post_info(self, post_id: str) -> dict:
		return requests.get(
			f"{self.api}/sydney/posts/{post_id}",
			headers=self.headers).json()

	def get_post_comments(
			self,
			post_id: str,
			page: int = 0,
			limit: int = 10) -> dict:
		return requests.get(
			f"{self.api}/sydney/posts/{post_id}/comments?page={page}&limit={limit}",
			headers=self.headers).json()

	def send_comment(
			self,
			post_id: str,
			content: str) -> dict:
		data = {
			"content": content
		}
		return requests.post(
			f"{self.api}/sydney/posts/{post_id}/comments",
			json=data,
			headers=self.headers).json()

	def delete_comment(
			self,
			post_id: str,
			comment_id: str) -> int:
		return requests.delete(
			f"{self.api}/sydney/posts/{post_id}/comments/{comment_id}",
			headers=self.headers).status_code

	def like_post(self, post_id: str) -> int:
		return requests.post(
			f"{self.api}/sydney/posts/{post_id}/likes",
			headers=self.headers).status_code

	def unlike_post(self, post_id: str) -> int:
		return requests.delete(
			f"{self.api}/sydney/posts/{post_id}/likes",
			headers=self.headers).status_code

	def create_post(
			self,
			description: str,
			images: list = [],
			videos: list = []) -> dict:
		data = {
			"description": description,
			"images": images,
			"videos": videos
		}
		return requests.post(
			f"{self.api}/sydney/posts",
			json=data,
			headers=self.headers).json()

	def delete_post(self, post_id: str) -> int:
		return requests.delete(
			f"{self.api}/sydney/posts/{post_id}",
			headers=self.headers).status_code

	def get_feed(self, limit: int = 10) -> dict:
		return requests.get(
			f"{self.api}/sydney/user-feed?limit={limit}",
			headers=self.headers).json()

	def get_notifications(self, page: int = 0, limit: int = 10) -> dict:
		return requests.get(
			f"{self.api}/sydney/users/{self.user_id}/notifications?page={page}&limit={limit}",
			headers=self.headers).json()
