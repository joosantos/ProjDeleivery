export default {
	getAccessToken,
	getRefreshToken,
	setAccessToken,
	setRefreshToken,
	clearTokens,
};

const ACCESS_TOKEN = "access_token";
const REFRESH_TOKEN = "refresh_token";

/**
 * Returns access token
 * @returns {string}
 */
function getAccessToken() {
	return localStorage.getItem(ACCESS_TOKEN);
}

/**
 * Returns refresh token
 * @returns {string}
 */
function getRefreshToken() {
	return localStorage.getItem(REFRESH_TOKEN);
}

/**
 * Set access token with the provided token
 * @param token
 */
function setAccessToken(token) {
	localStorage.setItem(ACCESS_TOKEN, token);
}

/**
 * Set refresh token with the provided token
 * @param refreshToken
 */
function setRefreshToken(refreshToken) {
	localStorage.setItem(REFRESH_TOKEN, refreshToken);
}

/**
 * Clear access and refresh tokens
 */
function clearTokens() {
	localStorage.removeItem(ACCESS_TOKEN);
	localStorage.removeItem(REFRESH_TOKEN);
}
