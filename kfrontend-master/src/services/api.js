import axios from "axios";
import router from "@/router";
import localStorageService from "./localStorage.service";
import authorizationService from "./authorization.service";
import store from "@/store";
import toast, { genericError } from "@/toast.js";

export { unauthApi, authApi, API_URL, errorHandling, translateDateFromApi };
const API_URL =
	import.meta.env.VITE_API_URL == undefined
		? "http://127.0.0.1:8000/"
		: import.meta.env.VITE_API_URL;

const HEADERS = {
	"Content-Type": "application/json",
};

const TIMEOUT = 25000;
const TIMEOUT_ERROR_MESSAGE = `timeout of ${TIMEOUT}ms exceeded`;

/**
 * Object for requests that doesn"t require authentication
 * @type {AxiosInstance}
 */
const unauthApi = axios.create({
	baseURL: API_URL,
	headers: HEADERS,
	timeout: TIMEOUT,
});

unauthApi.interceptors.response.use(
	(response) => {
		return response;
	},
	function (error) {
		const originalRequest = error.config;
		if (error.message === TIMEOUT_ERROR_MESSAGE) {
			return handleTimeout(originalRequest, error);
		}
		if (error.response == undefined || error.response == null || error.response.status >= 500) {
			return Promise.reject(error);
		}
		return Promise.reject(error);
	}
);

/**
 * Object for request that require authentication
 * @type {AxiosInstance}
 */
const authApi = axios.create({
	baseURL: API_URL,
	headers: HEADERS,
	timeout: TIMEOUT,
});

/**
 * Add access token to request
 */
authApi.interceptors.request.use((config) => {
	const token = localStorageService.getAccessToken();
	if (token) {
		config.headers.Authorization = `Bearer ${token}`;
	}
	return config;
});

/**
 * Interceptor for requests with access token
 * If any request returns 401 due to token expiration, call refresh, save new token and call original request again
 * If any other error or if refresh request returns error, redirect to login
 */
authApi.interceptors.response.use(
	(response) => {
		return response;
	},
	function (error) {
		const originalRequest = error.config;

		if (error.message === TIMEOUT_ERROR_MESSAGE) {
			return handleTimeout(originalRequest, error);
		}

		// if no response, return error
		if (error.response == undefined || error.response == null) {
			return Promise.reject(error);
		}

		// User Not Authenticated
		if (
			error.response.status === 401 ||
			(error.response.status === 422 &&
				(error.response.data.detail == "Signature has expired" ||
					error.response.data.detail == "Not enough segments"))
		) {
			if (originalRequest._retry) {
				toast.error("You need to login to procede");
				store.commit("setUser", null);
				router.push({ name: "Login" });
				return;
			}
			originalRequest._retry = true;

			if (localStorageService.getRefreshToken() == null) {
				toast.error("You need to login to procede");
				store.commit("setUser", null);
				router.push({ name: "Login" });
				return;
			}

			// call API to get a new token
			return authorizationService
				.refreshToken()
				.then((token) => {
					// update original request authorization header
					authApi.defaults.headers.common["Authorization"] = "Bearer " + token;

					// return originalRequest
					return authApi(originalRequest);
				})
				.catch(() => {
					Promise.reject(error);
				});
		}
		if (error.response.status === 403) {
			if (error.response.data.detail == "Email Not Verified") {
				store.commit("setUser", null);
				router.push({ name: "Verify Email" });
				return;
			}
			if (error.response.data.detail == "User Blocked") {
				store.commit("setUser", null);
				router.push({ name: "Block" });
				return;
			}
			if (error.response.data.detail == "Admin Not Verified") {
				store.commit("setUser", null);
				router.push({ name: "Verify Admin", params: { refuse: "false" } });
				return;
			}
			if (error.response.data.detail == "Admin Refuse") {
				store.commit("setUser", null);
				router.push({ name: "Verify Admin", params: { refuse: "true" } });
				return;
			}
			return Promise.reject(error);
		}
		// return any other error
		return Promise.reject(error);
	}
);

const handleTimeout = (originalRequest, error) => {
	if (originalRequest._timeoutRetries) {
		if (originalRequest._timeoutRetries === 1) {
			toast.warning("Server taking too long to respond, trying again...");
			originalRequest._timeoutRetries = 2;
			return authApi(originalRequest);
		} else {
			Promise.reject(error);
		}
	} else {
		originalRequest._timeoutRetries = 1;
		return authApi(originalRequest);
	}
};

const translateDateFromApi = function (dateFromApi) {
	let dateAux = "";
	if (dateFromApi != null) {
		let aux = dateFromApi.split("T")[0].split("-");
		dateAux = `${aux[2]}-${aux[1]}-${aux[0]}`;
	}
	return dateAux;
};

const errorHandling = function (error, showGeneric = true) {
	if (error == null || error.response == null) {
		genericError();
		throw error;
	}
	if (error?.response?.status >= 400 && error?.response?.status < 500) {
		if (error.response.data.detail == null || error.response.data.detail.length == 0) {
			genericError();
			return;
		}
		if (typeof error.response.data.detail === "string") toast.error(error.response.data.detail);
		else if (error.response.status === 422) {
			for (let err in error.response.data.detail) {
				toast.error(error.response.data.detail[err].msg);
			}
		} else {
			for (let err in error.response.data.detail) {
				toast.error(error.response.data.detail[err]);
			}
		}
		return;
	}

	if (showGeneric) {
		genericError();
	}
};
