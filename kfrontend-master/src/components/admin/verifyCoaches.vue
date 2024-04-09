<template>
	<Loading v-if="loading" :size="10" />
	<div v-else class="flex flex-col p-6 max-w-max mx-auto">
		<div class="overflow-x-auto min-w-max md:min-w-fit">
			<div
				:class="[
					'grid grid-cols-6 border-2 rounded-3xl border-blue-700 text-center space-x-4 divide-x-2 divide-blue-700 text-xl font-medium rounded-b-none',
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
					{{ t("verified.change") }}
				</div>
			</div>
			<div
				v-if="users.length == 0"
				class="grid grid-cols-6 border-2 border-t-0 border-blue-700 rounded-3xl rounded-t-none text-center space-x-4 divide-x-2 divide-blue-700">
				<div class="col-span-6 p-2 font-medium text-xl">{{ t("noUsers") }}</div>
			</div>
			<div
				v-for="(user, index) of users"
				:key="user.id"
				:class="[
					'grid grid-cols-6 border-2 border-t-0 border-blue-700 rounded-t-none text-center space-x-4 divide-x-2 divide-blue-700',
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
				<div class="col-span-1 px-2 py-1">
					{{
						user.admin_verified == null
							? t("verified.not")
							: user.admin_verified
							? user.admin_verified
							: t("verified.dennied")
					}}
				</div>
				<div class="col-span-1 px-2 py-1 inline-flex mx-auto justify-between">
					<div />
					<CheckIcon
						class="h-6 w-6 bg-green-200 text-green-600 rounded-full p-0.5 cursor-pointer"
						@click="updateCoach(user.id, true)" />
					<XMarkIcon
						class="h-6 w-6 bg-red-200 text-red-600 rounded-full p-0.5 cursor-pointer"
						@click="updateCoach(user.id, false)" />
					<div />
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import Loading from "@/components/partials/loading.vue";
import { CheckIcon, XMarkIcon } from "@heroicons/vue/24/solid";
import { useI18n } from "vue-i18n";
import { authApi } from "@/services/api";
import { ref } from "vue";
import { genericError } from "@/toast.js";

let users = ref([]);
let loading = ref(true);

let { t } = useI18n();

getUsers();

function getUsers() {
	authApi
		.get("/users/not-verified")
		.then((response) => {
			users.value = response.data;
			loading.value = false;
		})
		.catch(() => {
			genericError();
		});
}

function updateCoach(user_id, verified) {
	loading.value = true;
	authApi
		.put(`users/verify-coach/${user_id}`, { admin_verified: verified })
		.then(() => {
			getUsers();
		})
		.catch(() => {
			genericError();
		});
}
</script>

<i18n>
{
	"en_GB": {
		"name": "Name",
		"email": "Email",
		"verified": {
			"email": "Email Verified",
			"admin": "Verified by Admin",
			"not": "Not Verified Yet",
			"change": "Verify coach?",
			"dennied": "Access denied",
		},
		"false": "False",
		"true": "True",
		"noUsers": "There are no coaches left to verify"
	},
	"pt_PT": {
		"name": "Nome",
		"email": "Email",
		"verified": {
			"email": "Email Verificado",
			"admin": "Verificado pelo Administrador",
			"not": "Não foi verificado ainda",
			"change": "Verificar treinador?",
			"dennied": "Accesso negado",
		},
		"false": "Falso",
		"true": "Verdadeiro",
		"noUsers": "Não há mais treinadores para verificar"
	}
}
</i18n>
