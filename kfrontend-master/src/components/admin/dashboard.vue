<template>
	<div class="max-w-max flex-col p-4 mx-auto">
		<div class="flex flex-col flex-grow overflow-y-auto rounded-2xl bg-blue-200 px-8">
			<!-- Navbar links -->
			<div class="flex-grow flex flex-col">
				<nav class="py-6 space-y-4">
					<router-link
						v-for="item in navigation"
						:key="item.name"
						:to="{ name: item.route }"
						class="flex items-center p-2 font-medium rounded-md cursor-pointer hover:text-blue-900 text-blue-500 active:text-black">
						<div class="relative inline-flex mx-auto">
							<component
								:is="item.icon"
								class="mr-3 flex-shrink-0 h-8 w-8"
								aria-hidden="true" />
							<p :to="item.route" class="mx-auto text-2xl">
								{{ item.name }}
							</p>
							<div
								:class="[
									'text-sm bg-red-500 text-white rounded-full absolute z-10 text-center w-5 -right-4 -top-2',
									item.number == 0 ? 'hidden' : 'visible',
								]">
								{{ item.number }}
							</div>
						</div>
					</router-link>
				</nav>
			</div>
		</div>
	</div>
</template>

<script setup>
import {
	XCircleIcon,
	CheckCircleIcon,
	UserGroupIcon,
	WrenchIcon,
	UserIcon,
	PlusCircleIcon,
} from "@heroicons/vue/24/solid";
import { ref } from "vue";
import { authApi } from "@/services/api";
import { useI18n } from "vue-i18n";
import toast from "@/toast.js";

let { t } = useI18n();
let navigation = ref([
	{
		name: t("accept"),
		icon: CheckCircleIcon,
		route: "Verify Coaches",
		number: 0,
	},
	{
		name: t("block"),
		icon: XCircleIcon,
		route: "Block Coaches",
		number: 0,
	},
	{
		name: t("athlete.self", 2),
		icon: UserIcon,
		route: "Athletes Search",
		number: 0,
	},
	{
		name: t("teams"),
		icon: UserGroupIcon,
		route: "Teams",
		number: 0,
	},
	{
		name: t("coach"),
		icon: UserIcon,
		route: "Coaches",
		number: 0,
	},
	{
		name: t("insurances"),
		icon: PlusCircleIcon,
		route: "Insurances",
		number: 0,
	},
	{
		name: t("insurancesConfig"),
		icon: WrenchIcon,
		route: "Insurances Config",
		number: 0,
	},
]);
getUsers();
getFederationRequests();

function getUsers() {
	authApi
		.get("/users/not-verified")
		.then((response) => {
			navigation.value.find((a) => a.route == "Verify Coaches").number = response.data.length;
		})
		.catch(null);
}

function getFederationRequests() {
	authApi
		.get(`/insurances?year=${new Date().getFullYear()}&status=pending`)
		.then(({ data }) => {
			navigation.value.find((a) => a.route == "Insurances").number = data.n_results;
		})
		.catch((e) => {
			console.log(e);
		});
}
</script>

<i18n>
{
	"en_GB": {
		"accept": "Verify New Coaches",
		"block": "Block Coaches",
		"teams": "Teams",
		"insurancesConfig": "Insurances Config",
		"insurances": "Insurances",
		"coach": "Coaches",
		"federationRequests": "Federation Requests",
	},
	"pt_PT": {
		"accept": "Verificar novos treinadores",
		"block": "Bloquart Treinadores",
		"teams": "Equipas",
		"insurancesConfig": "Congigurar Seguros",
		"insurances": "Seguros",
		"coach": "Treinadores",
		"federationRequests": "Pedidos de Federação",
	}
}
</i18n>
