import { createApp } from "vue";
import App from "./App.vue";
import "./index.css";
import store from "./store/index.js";
import router from "./router/index.js";
import { createI18n } from "vue-i18n";
import Toast from "vue-toastification";
import "vue-toastification/dist/index.css";
import { registerScrollSpy } from "vue3-scroll-spy";
import VueTheMask from "vue-the-mask";
import messages from "@intlify/unplugin-vue-i18n/messages";

const i18n = createI18n({
	legacy: false,
	globalInjection: true,
	locale: "en_GB",
	fallbackLocale: "en_GB",
	availableLocales: ["en_GB", "pt_PT"],
	messages: messages,
});

const app = createApp(App).use(store).use(router).use(i18n).use(VueTheMask).use(Toast, {
	transition: "Vue-Toastification__bounce",
	maxToasts: 20,
	newestOnTop: true,
	timeout: 7000,
});

registerScrollSpy(app);

app.mount("#app");
