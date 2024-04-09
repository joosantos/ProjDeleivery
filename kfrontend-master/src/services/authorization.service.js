import localStorageService from "./localStorage.service";
import { unauthApi } from "./api";

const URL = "auth/";

export default {
	refreshToken,
	doLogin,
	logout,
	isAuthenticated,
};

/**
 * Do login with the provided username and password
 * @param username
 * @param password
 * @returns {Promise<AxiosResponse<any>>}
 */
function doLogin(username, password) {
	const config = {
		headers: {
			"Content-Type": "application/x-www-form-urlencoded",
		},
	};

	const params = new URLSearchParams();
	params.append("username", username);
	params.append("password", password);

	return unauthApi.post(URL + "login", params, config).then((response) => {
		// save new token to LocalStorage
		localStorageService.setAccessToken(response.data.access_token);
		localStorageService.setRefreshToken(response.data.refresh_token);
	});
}

function logout() {
	localStorageService.clearTokens();
}

/**
 * Call refresh token action, save new access token
 * @returns {Promise<((path: PathLike, mode: (number | undefined), callback: NoParamCallback) => void) | ((path: PathLike, callback: NoParamCallback) => void) | ((path: PathLike, mode?: number) => Promise<void>) | access | "public" | "private" | "protected">}
 */
function refreshToken() {
	// call API to get a new token
	return (
		unauthApi
			.post(URL + "refresh", {
				refresh_token: localStorageService.getRefreshToken(),
			})
			.then((response) => {
				// save new token to LocalStorage
				localStorageService.setAccessToken(response.data.access_token);
				return Promise.resolve(response.data.access);
			})
			// In case refresh token call returns an error, clear tokens and redirect to login
			.catch((error) => {
				localStorageService.clearTokens();
				return Promise.reject(error);
			})
	);
}

/**
 * Checks if user is authenticated based on local storage tokens.
 * NOTE: Ideally it would call API to check token (and refresh token, if necessary)
 * @returns {boolean|boolean}
 */
function isAuthenticated() {
	//TODO: Call api to check tokens
	return !!localStorageService.getAccessToken() && !!localStorageService.getRefreshToken();
}
