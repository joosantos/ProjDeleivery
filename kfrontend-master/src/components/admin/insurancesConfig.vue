<template>
	<InsuranceTypeModal
		:open="openModalInsuranceType"
		:insurance-type-id="modalInsuranceTypeId"
		@updated="getInsuranceTypes"
		@close="
			modalInsuranceTypeId = '';
			openModalInsuranceType = false;
		" />
	<InsuranceGroupModal
		:open="openModalInsuranceGroup"
		:insurance-group-id="modalInsuranceGroupId"
		@updated="getInsuranceGroups"
		@close="
			modalInsuranceGroupId = '';
			openModalInsuranceGroup = false;
		" />
	<Loading v-if="loading" :size="10" />
	<div v-else class="grid grid-cols-2 space-x-8">
		<div class="col-span-2 md:col-span-1">
			<p class="text-center font-semibold text-2xl">{{ t("insuranceTypes") }}</p>
			<Loading v-if="loadingInsuranceTypes" :size="10" />
			<div v-else class="mt-4 grid grid-cols-2 gap-x-4 gap-y-2">
				<div
					v-for="insuranceType of insuranceTypes"
					:key="insuranceType.id"
					class="w-full rounded-full bg-blue-100 px-8 py-2">
					<div class="inline-flex justify-between w-full">
						<p class="text-2xl font-medium">{{ insuranceType.name }}</p>
						<p>
							{{ t("fee", { fee: insuranceType.fee }) }}
						</p>
					</div>
					<div class="inline-flex justify-between w-full">
						<p>
							{{
								insuranceType.description.length > 124
									? `${insuranceType.description.substring(0, 120)}...`
									: insuranceType.description
							}}
						</p>
						<div class="my-auto">
							<button
								class="w-7 p-1 rounded-lg border border-yellow-600 bg-yellow-200 text-yellow-600 hover:bg-yellow-400"
								@click="
									modalInsuranceTypeId = insuranceType.id;
									openModalInsuranceType = true;
								">
								<PencilIcon />
							</button>
						</div>
					</div>
				</div>
				<button
					class="col-span-full rounded-full bg-green-100 px-8 py-2 border border-green-300 hover:bg-green-200 hover:border-green-500"
					@click="openModalInsuranceType = true">
					<div class="text-lg font-medium inline-flex">
						<PlusIcon class="h-5 w-5 mt-1 mr-2" />
						<p>{{ t("newInsuranceType") }}</p>
					</div>
				</button>
			</div>
		</div>
		<div class="col-span-2 md:col-span-1">
			<p class="text-center font-semibold text-2xl">{{ t("insuranceGroups") }}</p>
			<Loading v-if="loadingInsuranceGroups" :size="10" />
			<div v-else class="mt-4 grid grid-cols-2 gap-x-4 gap-y-2">
				<div
					v-for="insuranceGroup of insuranceGroups"
					:key="insuranceGroup.id"
					class="w-full rounded-full bg-blue-100 px-8 py-2">
					<div class="inline-flex w-full">
						<div class="flex-col flex justify-between w-full">
							<p class="text-2xl font-medium w-full">{{ insuranceGroup.name }}</p>
							<p>
								{{
									insuranceGroup.description.length > 124
										? `${insuranceGroup.description.substring(0, 120)}...`
										: insuranceGroup.description
								}}
							</p>
						</div>
						<div class="my-auto">
							<button
								class="w-7 p-1 rounded-lg border border-yellow-600 bg-yellow-200 text-yellow-600 hover:bg-yellow-400"
								@click="
									modalInsuranceGroupId = insuranceGroup.id;
									openModalInsuranceGroup = true;
								">
								<PencilIcon />
							</button>
						</div>
					</div>
				</div>
				<button
					class="col-span-full rounded-full bg-green-100 px-8 py-2 border border-green-300 hover:bg-green-200 hover:border-green-500"
					@click="openModalInsuranceGroup = true">
					<div class="text-lg font-medium inline-flex">
						<PlusIcon class="h-5 w-5 mt-1 mr-2" />
						<p>{{ t("newInsuranceGroup") }}</p>
					</div>
				</button>
			</div>
		</div>
	</div>
</template>

<script setup>
import Loading from "@/components/partials/loading.vue";
import InsuranceTypeModal from "@/components/admin/modals/insuranceType.vue";
import InsuranceGroupModal from "@/components/admin/modals/insuranceGroup.vue";
import { ref } from "vue";
import { authApi, errorHandling } from "@/services/api";
import { PlusIcon } from "@heroicons/vue/24/outline";
import { PencilIcon } from "@heroicons/vue/24/solid";
import { useI18n } from "vue-i18n";

let { t } = useI18n({ useScope: "global" });

let insuranceTypes = ref([]);
let insuranceGroups = ref([]);
let loading = ref(true);
let loadingInsuranceTypes = ref(false);
let loadingInsuranceGroups = ref(false);
let openModalInsuranceType = ref(false);
let modalInsuranceTypeId = ref("");
let openModalInsuranceGroup = ref(false);
let modalInsuranceGroupId = ref("");

let initialPromises = [];
initialPromises.push(
	authApi.get("insurance-types").then((response) => {
		insuranceTypes.value = response.data;
	})
);
initialPromises.push(
	authApi.get("insurance-groups").then((response) => {
		insuranceGroups.value = response.data;
	})
);

Promise.all(initialPromises)
	.then(() => {
		loading.value = false;
	})
	.catch((error) => {
		errorHandling(error);
	});

function getInsuranceTypes() {
	loadingInsuranceTypes.value = true;
	authApi
		.get("insurance-types")
		.then((response) => {
			loadingInsuranceTypes.value = false;
			insuranceTypes.value = response.data;
		})
		.catch((error) => {
			errorHandling(error);
		});
}

function getInsuranceGroups() {
	loadingInsuranceGroups.value = true;
	authApi
		.get("insurance-groups")
		.then((response) => {
			loadingInsuranceGroups.value = false;
			insuranceGroups.value = response.data;
		})
		.catch((error) => {
			errorHandling(error);
		});
}
</script>
