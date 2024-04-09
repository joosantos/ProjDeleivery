<template>
	<Loading v-if="loading" :size="10" />
	<div v-else class="flex flex-col p-6 max-w-max mx-auto">
		<p class="text-center text-4xl font-semibold">{{ t("blockTitle") }}</p>
		<div class="inline-flex mx-auto space-x-8 mt-4 mb-4">
			<ToogleInput
				:label="t('labels.showAll')"
				:name="'showAll'"
				:option-selected="state.showAll"
				:error="''"
				@value-changed="
					(option) => {
						state.showAll = option;
						filterCoaches();
					}
				" />
		</div>
		<div v-if="!state.showAll" class="inline-flex mx-auto space-x-8 mb-4">
			<ToogleInput
				:label="t('labels.showVerified')"
				:name="'showVerified'"
				:option-selected="state.showVerified"
				:error="''"
				@value-changed="
					(option) => {
						state.showVerified = option;
						filterCoaches();
					}
				" />
			<ToogleInput
				:label="t('labels.showBlocked')"
				:name="'showBlocked'"
				:option-selected="state.showBlocked"
				:error="''"
				@value-changed="
					(option) => {
						state.showBlocked = option;
						filterCoaches();
					}
				" />
		</div>
		<div class="overflow-x-auto min-w-max md:min-w-fit">
			<div
				:class="[
					'grid grid-cols-7 border-2 rounded-3xl border-blue-700 text-center space-x-4 divide-x-2 divide-blue-700 text-xl font-medium rounded-b-none',
				]">
				<div class="col-span-1 p-2">
					{{ t("name") }}
				</div>
				<div class="col-span-2 p-2">
					{{ t("email") }}
				</div>
				<div class="col-span-1 p-2">
					{{ t("verified.email") }}
				</div>
				<div class="col-span-1 p-2">
					{{ t("verified.admin") }}
				</div>
				<div class="col-span-1 p-2">
					{{ t("active") }}
				</div>
				<div class="col-span-1 p-2">
					{{ t("block") }}
				</div>
			</div>
			<div
				v-if="users.length == 0"
				class="grid grid-cols-6 border-2 border-t-0 border-blue-700 rounded-3xl rounded-t-none text-center space-x-4 divide-x-2 divide-blue-700">
				<div class="col-span-6 p-2 font-medium text-xl">{{ t("noUsers") }}</div>
			</div>
			<div
				v-for="(user, index) of users"
				v-show="user.show"
				:key="user.id"
				:class="[
					'grid grid-cols-7 border-2 border-t-0 border-blue-700 rounded-t-none text-center space-x-4 divide-x-2 divide-blue-700',
					index == users.length - 1 ? 'rounded-3xl' : '',
				]">
				<div class="col-span-1 px-2 py-1">
					{{ user.name }}
				</div>
				<div class="col-span-2 px-2 py-1">
					{{ user.email }}
				</div>
				<div class="col-span-1 px-2 py-1">
					{{ t(user.email_verified.toString()) }}
				</div>
				<div
					:class="[
						'col-span-1 px-2 py-1',
						user.admin_verified ? 'text-green-500' : 'text-red-500',
					]">
					{{
						user.admin_verified == null
							? t("verified.not")
							: user.admin_verified
							? t("verified.accepted")
							: t("verified.dennied")
					}}
				</div>
				<div
					:class="[
						'col-span-1 px-2 py-1',
						user.is_active ? 'text-red-500' : 'text-green-500',
					]">
					{{ t((!user.is_active).toString()) }}
				</div>
				<div class="col-span-1 px-2 py-1 inline-flex mx-auto justify-between">
					<div />
					<CheckIcon
						class="h-6 w-6 bg-green-200 text-green-600 rounded-full p-0.5 cursor-pointer"
						@click="updateUser(user.id, false)" />
					<XMarkIcon
						class="h-6 w-6 bg-red-200 text-red-600 rounded-full p-0.5 cursor-pointer"
						@click="updateUser(user.id, true)" />
					<div />
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import Loading from "@/components/partials/loading.vue";
import ToogleInput from "@/components/partials/inputs/toogle.vue";
import { CheckIcon, XMarkIcon } from "@heroicons/vue/24/solid";
import { useI18n } from "vue-i18n";
import { authApi, errorHandling } from "@/services/api";
import { ref } from "vue";

let users = ref([]);
let loading = ref(true);
let state = ref({
	showVerified: false,
	showBlocked: false,
	showAll: true,
});
let { t } = useI18n();

getUsers();

function getUsers() {
	authApi
		.get("/users?limit=-1&is_coach=true")
		.then((response) => {
			users.value = response.data.results;
			for (let user of users.value) {
				user.show = true;
			}
			loading.value = false;
		})
		.catch((error) => {
			errorHandling(error);
		});
}

function updateUser(user_id, verified) {
	loading.value = true;
	authApi
		.put(`users/update-block/${user_id}`, { is_active: verified })
		.then(() => {
			getUsers();
		})
		.catch((error) => {
			errorHandling(error);
		});
}

function filterCoaches() {
	if (state.value.showAll) {
		for (let user of users.value) {
			user.show = true;
		}
		return;
	}
	for (let user of users.value) {
		user.show =
			!user.is_active == state.value.showBlocked &&
			user.admin_verified == state.value.showVerified;
	}
}
</script>

<i18n>
{
	"en_GB": {
		"blockTitle": "Block Coaches",
		"name": "Name",
		"email": "Email",
		"verified": {
			"email": "Email Verified",
			"admin": "Verified by Admin",
			"not": "Not Verified Yet",
			"dennied": "Access denied",
			"accepted": "Access granted",
		},
		"labels": {
			"showVerified": "Show Verified Coaches",
			"showBlocked": "Show Blocked Coaches",
			"showAll": "Show All"
		},
		"active": "Blocked",
		"block": "Block?",
		"false": "False",
		"true": "True",
		"noUsers": "There are no coaches left to verify"
	},
	"pt_PT": {
		"blockTitle": "Bloquear Treinadores",
		"name": "Nome",
		"email": "Email",
		"verified": {
			"email": "Email Verificado",
			"admin": "Verificado pelo Administrador",
			"not": "Não foi verificado ainda",
			"change": "Verificar treinador?",
			"dennied": "Accesso negado",
			"accepted": "Access concedido",
		},
		"labels": {
			"showVerified": "Mostrar Treinadores Verificados",
			"showBlocked": "Mostrar Treinadores Bloqueados",
			"showAll": "Mostrar Todos"
		},
		"false": "Falso",
		"true": "Verdadeiro",
		"noUsers": "Não há mais treinadores para verificar"
	}
}
</i18n>
