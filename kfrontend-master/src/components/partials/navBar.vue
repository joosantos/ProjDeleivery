<template>
	<div class="w-full">
		<!-- Static sidebar for desktop -->
		<div
			v-if="store.getters.getShowNavBar"
			class="hidden lg:inline-flex w-full lg:fixed lg:inset-x-0 p-4 z-[15] relative">
			<div class="inline-flex w-full rounded-full bg-blue-200">
				<div class="bg-white -z-10 inset-0 w-full h-full absolute" />
				<!-- Logotipo -->
				<router-link
					class="flex items-center flex-shrink-0 p-2 cursor-pointer ml-4"
					:to="{ name: 'Home' }">
					<img class="h-14 w-auto rounded-full" src="/logo.png" alt="APLK Logo" />
				</router-link>

				<!-- Navbar links -->
				<nav class="inline-flex p-4 ml-20">
					<NavBarItem
						v-for="(nav, index) of store.getters.getUser == null ? notLogged : logged"
						v-show="
							nav.show[0] == 'all' ||
							nav.show.indexOf(store.getters.getUserRole) != -1
						"
						:key="nav.name"
						:class="['ml-5', index == notLogged.length - 1 && 'mr-auto']"
						:route="nav.route"
						:name="nav.name"
						:icon="nav.icon"
						:outline="nav.outline"
						:current="nav.current" />
				</nav>

				<!-- Language Select -->
				<div class="ml-auto my-auto">
					<select
						id="locale"
						v-model="locale"
						name="locale"
						style="-moz-appearance: none"
						class="appearance-none border-blue-600 border-2 text-black bg-transparent rounded-full">
						<option value="en_GB">
							{{ countriesList.getEmojiFlag("GB") + " English" }}
						</option>
						<option value="pt_PT">
							{{ countriesList.getEmojiFlag("PT") + " Português" }}
						</option>
					</select>
				</div>

				<!-- User name -->
				<div
					v-if="store.getters.getUser != null"
					class="items-center flex-shrink-0 px-4 text-center my-auto">
					<p>
						<span
							v-if="store.getters.getUser.user_role.role.name === 'COACH'"
							class="font-bold">
							{{ t("navBar.coach") }}
						</span>
						{{ store.getters.getUser.name }}
					</p>
				</div>

				<!-- Gray Divide -->
				<div class="h-full ml-4">
					<div class="bg-gray-500 h-2/3 w-px mt-4" />
				</div>

				<!-- Sign in links -->
				<div v-if="store.getters.getUser == null" class="inline-flex p-4 space-x-4 mr-4">
					<NavBarItem
						route="Login"
						:name="t('navBar.login')"
						:icon="ArrowRightOnRectangleIcon" />
					<NavBarItem
						route="Register"
						:name="t('navBar.register')"
						:icon="ClipboardDocumentListIcon" />
				</div>

				<!-- Sign out link -->
				<div
					v-else
					class="cursor-pointer items-center flex-shrink-0 px-4 mr-4 text-center inline-flex"
					@click="logout">
					<ArrowLeftOnRectangleIcon class="w-5 h-5" />
					<p class="ml-2 mt-px">
						{{ t("navBar.signOut") }}
					</p>
				</div>
			</div>
		</div>
		<div v-if="store.getters.getShowNavBar" class="h-1 hidden md:block" />
		<div v-if="store.getters.getShowNavBar" class="hidden lg:block h-[7.5rem]" />

		<!-- Navbar for small screens -->
		<!-- Topbar -->
		<div
			v-if="store.getters.getShowNavBar"
			class="top-0 z-10 flex-shrink-0 flex lg:hidden h-16">
			<div class="flex-1 px-4 flex justify-between">
				<router-link
					class="flex flex-1 w-full lg:ml-0 cursor-pointer"
					:to="{ name: 'Home' }">
					<img
						class="h-8 w-8 rounded-full place-self-center"
						src="/logo.png"
						alt="LTKP Logo" />
				</router-link>
				<div class="ml-4 flex items-center lg:ml-6">
					<!-- Profile dropdown -->
					<Menu as="div" class="ml-3 relative z-40">
						<div>
							<MenuButton
								class="max-w-xs bg-white flex items-center text-sm rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
								<span class="sr-only"> Open user menu </span>
								<img class="h-8 w-8 rounded-full" src="/blank_avatar.png" alt="" />
							</MenuButton>
						</div>
						<transition
							enter-active-class="transition ease-out duration-100"
							enter-from-class="transform opacity-0 scale-95"
							enter-to-class="transform opacity-100 scale-100"
							leave-active-class="transition ease-in duration-75"
							leave-from-class="transform opacity-100 scale-100"
							leave-to-class="transform opacity-0 scale-95">
							<MenuItems
								v-if="store.getters.getUser == null"
								class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none">
								<MenuItem>
									<router-link
										class="px-4 py-2 text-sm text-gray-700 inline-flex cursor-pointer hover:bg-gray-200 w-full"
										:to="{ name: 'Login' }">
										<ArrowRightOnRectangleIcon class="w-5 h-5" />
										<p class="ml-2">
											{{ t("navBar.login") }}
										</p>
									</router-link>
								</MenuItem>
								<MenuItem>
									<router-link
										class="px-4 py-2 text-sm text-gray-700 inline-flex cursor-pointer hover:bg-gray-200 w-full"
										:to="{ name: 'Register' }">
										<ClipboardDocumentListIcon class="w-5 h-5" />
										<p class="ml-2">
											{{ t("navBar.register") }}
										</p>
									</router-link>
								</MenuItem>
							</MenuItems>
							<MenuItems
								v-else
								class="origin-top-right absolute right-0 mt-2 w-48 rounded-md shadow-lg py-1 bg-white ring-1 ring-black ring-opacity-5 focus:outline-none">
								<MenuItem>
									<div
										class="px-4 py-2 text-sm text-gray-700 inline-flex cursor-pointer hover:bg-gray-200 w-full"
										@click="logout()">
										<ArrowLeftOnRectangleIcon class="w-5 h-5" />
										<p class="ml-2">
											{{ t("navBar.signOut") }}
										</p>
									</div>
								</MenuItem>
							</MenuItems>
						</transition>
					</Menu>
				</div>
			</div>
		</div>
		<div :class="['select-auto', store.getters.getShowMargins ? 'px-6' : 'px-0']">
			<slot></slot>
		</div>
		<div v-if="store.getters.getShowNavBar" class="h-24" />

		<!-- Footer -->
		<footer
			v-if="store.getters.getShowNavBar"
			:class="[
				'text-center p-4 w-full absolute bottom-0 duration-300',
				showNavBar ? 'opacity-0 lg:opacity-100' : '',
			]">
			<address class="bg-blue-100 py-4 rounded-full not-italic">
				{{ t("footer.dev") }}
				<a href="mailto:miguelangeloleal@hotmail.com">Miguel Jesus</a>
				| {{ t("footer.contact") }}:
				<a href="mailto:miguelangeloleal@hotmail.com">miguelangeloleal@hotmail.com</a>
			</address>
		</footer>

		<!-- Navbar for small screens -->
		<!-- Bottombar -->
		<div
			v-if="store.getters.getShowNavBar"
			:class="[
				'flex lg:hidden flex-col flex-grow fixed w-full bottom-0 z-10 flex-shrink-0 h-16 duration-200 bg-blue-200',
				showNavBar ? 'bottom-0' : '-bottom-16',
			]">
			<div class="w-full inline-flex my-auto">
				<!-- Navbar links -->
				<router-link
					v-for="nav in store.getters.getUser == null ? notLogged : logged"
					v-show="
						nav.show[0] == 'all' ||
						nav.show.indexOf(store.getters.getUser.user_role.role.name) != -1
					"
					:key="nav.name"
					class="w-full text-center relative"
					:to="{ name: nav.route }"
					@click="nav.current ? scrollToTop() : null">
					<div
						:class="[
							'inline-flex items-center py-1 rounded-full font-medium cursor-pointer',
							nav.current ? 'bg-blue-400' : 'active:bg-blue-400',
							nav.current ? 'px-4 transform duration-500' : 'px-0',
						]">
						<component
							:is="nav.current ? nav.icon : nav.outline"
							class="mx-auto flex-shrink-0 h-6 w-6"
							aria-hidden="true" />
					</div>
					<span
						v-if="false"
						class="absolute top-0 right-1/3 translate-x-1/2 items-center px-2 py-0.5 rounded-full text-xs bg-red-500 text-white">
						1
					</span>
					<p :to="nav.route" class="mx-auto -mt-1">
						{{ nav.name }}
					</p>
				</router-link>
			</div>
		</div>
	</div>
</template>

<script setup>
import NavBarItem from "@/components/partials/navBarItem.vue";
import { Menu, MenuButton, MenuItem, MenuItems } from "@headlessui/vue";
import {
	BuildingLibraryIcon,
	ComputerDesktopIcon,
	ClipboardDocumentCheckIcon,
	MicrophoneIcon,
} from "@heroicons/vue/24/solid";
import {
	BuildingLibraryIcon as BuildingLibraryIconOutlined,
	ComputerDesktopIcon as ComputerDesktopIconOutlined,
	ClipboardDocumentCheckIcon as ClipboardDocumentCheckIconOutlined,
	ClipboardDocumentListIcon,
	ArrowLeftOnRectangleIcon,
	ArrowRightOnRectangleIcon,
	MicrophoneIcon as MicrophoneIconOutlined,
} from "@heroicons/vue/24/outline";
import { ref, watch } from "vue";
import store from "@/store";
import router from "@/router";
import localStorageService from "@/services/localStorage.service";
import { useI18n } from "vue-i18n";
import countriesList from "countries-list";

let { t, locale } = useI18n({ useScope: "global" });

// Links of the Sidebar
let notLogged = ref([
	{
		name: "navBar.competition",
		icon: BuildingLibraryIcon,
		outline: BuildingLibraryIconOutlined,
		route: "Competition",
		current: false,
		show: ["all"],
	},
]);
let logged = ref([
	{
		name: "navBar.competition",
		icon: BuildingLibraryIcon,
		outline: BuildingLibraryIconOutlined,
		route: "Competition",
		current: false,
		show: ["all"],
	},
	{
		name: "navBar.dashboard.coach",
		icon: ComputerDesktopIcon,
		outline: ComputerDesktopIconOutlined,
		route: "Coach Dashboard",
		current: false,
		show: ["COACH"],
	},
	{
		name: "navBar.dashboard.combatManager",
		icon: ClipboardDocumentCheckIcon,
		outline: ClipboardDocumentCheckIconOutlined,
		route: "Combat Competition",
		current: false,
		show: ["AREA"],
	},
	{
		name: "navBar.dashboard.combatPublic",
		icon: ComputerDesktopIcon,
		outline: ComputerDesktopIconOutlined,
		route: "Template Combat",
		current: false,
		show: ["AREA"],
	},
	{
		name: "navBar.dashboard.admin",
		icon: ClipboardDocumentCheckIcon,
		outline: ClipboardDocumentCheckIconOutlined,
		route: "Admin Dashboard",
		current: false,
		show: ["ADMIN"],
	},
	{
		name: "navBar.dashboard.microphone",
		icon: MicrophoneIcon,
		outline: MicrophoneIconOutlined,
		route: "Microphone Competition",
		current: false,
		show: ["MICRO"],
	},
	{
		name: "navBar.dashboard.podium",
		icon: ComputerDesktopIcon,
		outline: ComputerDesktopIconOutlined,
		route: "Podium Competition",
		current: false,
		show: ["PODIUM"],
	},
]);

// Saves wich element of the navigation is the current if any
watch(
	() => router.currentRoute.value,
	(to) => {
		for (let nav of [...notLogged.value, ...logged.value]) {
			nav.current = nav.route == to.name;

			if (
				["MICRO", "PODIUM"].findIndex((a) => a == store.getters.getUserRole) !== -1 &&
				["Microphone", "Podium"].findIndex((a) => to.name.indexOf(a) !== -1) !== -1 &&
				["Microphone", "Podium"].findIndex((a) => nav.route.indexOf(a) !== -1) !== -1
			) {
				nav.current = true;
			}
		}
	}
);

// Updates nav bar names
watch(
	() => locale.value,
	() => {
		localStorage.setItem("local-language", locale.value);
	}
);

// Logouts the user
function logout() {
	localStorageService.clearTokens();
	store.commit("setUser", null);
	router.push({ name: "Home" });
}

// Scroll to top of the page
function scrollToTop() {
	window.scrollTo({ top: 0, behavior: "smooth" });
}

let prevScrollpos = window.pageYOffset;
let showNavBar = ref(true);
window.onscroll = function () {
	let currentScrollPos = window.pageYOffset;
	if (prevScrollpos > currentScrollPos) {
		showNavBar.value = true;
	} else {
		showNavBar.value = false;
	}
	prevScrollpos = currentScrollPos;
};
</script>
