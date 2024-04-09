<template>
	<div>
		<ChooseNewInsuranceTypeModal
			:open="openNewInsuranceModal"
			:teamId="props.teamId"
			@close="openNewInsuranceModal = false">
		</ChooseNewInsuranceTypeModal>
		<router-link :to="{ name: 'Team View', params: { teamId: props.teamId } }">
			<Button
				class="max-w-max mt-4"
				:message="t('returnToTeamView')"
				:type="'primary'"
				:pill="true"
				:iconLeft="true"
				:icon="ArrowLeftIcon"
				@button-click="null" />
		</router-link>
		<p class="text-2xl font-semibold">Insurances</p>
		<div class="inline-flex w-full justify-between">
			<form @submit.prevent="getInsurances" class="inline-flex w-full space-x-8">
				<CustomInput
					:type="'text'"
					:mask="'####'"
					:name="'insuranceYear'"
					:label="t('insurancesCoveringYear')"
					:option-selected="insuranceYear"
					:error="''"
					@value-changed="(option) => (insuranceYear = option)" />
				<div>
					<Button
						class="max-w-max px-8 relative top-1/2 -translate-y-1/2"
						:message="t('forms.search')"
						:type="'primary'"
						:pill="true"
						:size="'small'"
						:submit="true"
						:up-on-hover="false"
						@button-click="null" />
				</div>
			</form>
			<div>
				<div v-if="selectInsurancesForPaymentGuide" class="space-x-8 inline-flex">
					<Button
						class="min-w-max max-w-max"
						:message="t('getPaymentGuide')"
						:type="'primary'"
						:pill="true"
						:loading="loadingDownloadPaymentGuide"
						@button-click="getPaymentGuide" />
					<Button
						class="max-w-max"
						:message="t('cancel')"
						:type="'danger'"
						:pill="true"
						:up-on-hover="false"
						:disabled="loadingDownloadPaymentGuide"
						@button-click="() => (selectInsurancesForPaymentGuide = false)" />
				</div>
				<Button
					v-else
					class="min-w-max max-w-max"
					:message="t('selectInsurancesForPaymentGuide')"
					:type="'primary'"
					:pill="true"
					:disabled="selectGroupsToSendPaymentComprovative"
					@button-click="selectInsurancesForPaymentGuide = true" />
			</div>
		</div>

		<div class="inline-flex w-full justify-between mt-4">
			<div>
				<Button
					v-if="!selectGroupsToSendPaymentComprovative"
					class="max-w-max"
					:message="t('selectInsurancesToSendPaymentComprovative')"
					:type="'primary'"
					:pill="true"
					:up-on-hover="false"
					:disabled="selectInsurancesForPaymentGuide"
					@button-click="() => (selectGroupsToSendPaymentComprovative = true)" />
				<div v-else class="space-x-8 inline-flex">
					<FileInput
						class="max-w-max"
						:name="'paymentComprovative'"
						:label="t('paymentComprovative')"
						:error="''"
						@value-changed="(option) => (paymentComprovative = option)" />
					<Button
						class="max-w-max"
						:message="t('sendPaymentComprovative')"
						:type="'primary'"
						:pill="true"
						:up-on-hover="false"
						:loading="loadingUploadPaymentComprovative"
						@button-click="sendPaymentComprovative" />
					<Button
						class="max-w-max"
						:message="t('cancel')"
						:type="'danger'"
						:pill="true"
						:disabled="loadingUploadPaymentComprovative"
						:up-on-hover="false"
						@button-click="() => (selectGroupsToSendPaymentComprovative = false)" />
				</div>
			</div>
			<Button
				class="max-w-max"
				:message="t('createNewInsuranceRequest')"
				:type="'success'"
				:pill="true"
				:up-on-hover="false"
				:icon-left="true"
				:icon="PlusIcon"
				@button-click="openNewInsuranceModal = true" />
		</div>
		<Loading v-if="loading" :size="10" />
		<div
			v-else
			class="grid 2xl:grid-cols-6 lg:grid-cols-4 sm:grid-cols-2 grid-cols-1 justify-center gap-y-4 gap-x-4 mt-4">
			<div
				v-for="insurance in insurances"
				:key="insurance.sub_team_group"
				:class="[
					'mx-auto border rounded-lg px-4 py-2 w-full relative',
					selectGroupsToSendPaymentComprovative || selectInsurancesForPaymentGuide
						? 'cursor-pointer'
						: 'bg-blue-100 border-blue-300',
					selectGroupsToSendPaymentComprovative
						? groupsToSendPaymentComprovative.findIndex(
								(a) => a === insurance.sub_team_group
						  ) === -1
							? 'bg-blue-100 hover:bg-blue-200 border-blue-300'
							: 'bg-indigo-300 border-indigo-500 hover:bg-indigo-400'
						: '',
					selectInsurancesForPaymentGuide
						? groupsToGetPaymentGuide.findIndex(
								(a) => a === insurance.sub_team_group
						  ) === -1
							? 'bg-blue-100 hover:bg-blue-200 border-blue-300'
							: 'bg-yellow-300 border-yellow-500 hover:bg-yellow-400'
						: '',
				]"
				@click="
					selectGroupsToSendPaymentComprovative
						? toogleGroupToSendPaymentComprovatives(insurance.sub_team_group)
						: selectInsurancesForPaymentGuide
						? toogleGroupToGetPaymentGuide(insurance.sub_team_group)
						: null
				">
				<router-link
					:to="{
						name: 'Insurance Request Details',
						params: { teamId: props.teamId, subTeamGroup: insurance.sub_team_group },
					}"
					class="absolute w-7 h-7 top-2 right-2 p-1 rounded-lg border border-yellow-600 bg-yellow-200 text-yellow-600 hover:bg-yellow-400">
					<PencilIcon />
				</router-link>
				<p class="text-xl font-semibold text-center line-clamp-1">
					{{ insurance.insurance_type.name }}
				</p>
				<br />
				<p class="text-lg font-medium">
					{{
						insurance.insurance_type.name === "Team"
							? t("teamInsurance")
							: t("athletesInThisGroup", { number: insurance.number_insured })
					}}
				</p>
				<div class="w-full">
					<p>{{ t("medicalExams") }}</p>
					<LoadingBar
						:size="'small'"
						:progress="
							(insurance.number_medical_exams * 100) / insurance.number_insured
						"
						:variant="
							insurance.number_medical_exams === insurance.number_insured
								? 'success'
								: 'warning'
						" />
					<p class="text-center w-full">
						{{
							t("numberOfNumber", {
								number1: insurance.number_medical_exams,
								number2: insurance.number_insured,
							})
						}}
					</p>
				</div>
				<div class="w-full">
					<p>
						{{ t("missingPaymentComprovative") }}
					</p>
					<LoadingBar
						:size="'small'"
						:progress="
							(insurance.number_payment_comprovatives * 100) /
							insurance.number_insured
						"
						:variant="
							insurance.number_payment_comprovatives === insurance.number_insured
								? 'success'
								: 'warning'
						" />
					<p class="text-center w-full">
						{{
							t("numberOfNumber", {
								number1: insurance.number_payment_comprovatives,
								number2: insurance.number_insured,
							})
						}}
					</p>
				</div>
				<div class="w-full">
					<p>{{ t("requestsStatus") }}</p>
					<div class="grid grid-cols-1 w-full">
						<div class="inline-flex">
							<div class="w-4 mt-1 h-4 rounded-full bg-red-500"></div>
							<p class="ml-2">
								{{ t("federationRequest.other", insurance.number_other_status) }}
							</p>
						</div>
						<div class="inline-flex">
							<div class="w-4 mt-1 h-4 rounded-full bg-blue-500"></div>
							<p class="ml-2">
								{{ t("federationRequest.pending", insurance.number_pending) }}
							</p>
						</div>
						<div class="inline-flex">
							<div class="w-4 mt-1 h-4 rounded-full bg-green-500"></div>
							<p class="ml-2">
								{{ t("federationRequest.accepted", insurance.number_accepted) }}
							</p>
						</div>
					</div>
					<MultipleLoadingBar
						:size="'small'"
						:bars="[
							{
								progress:
									(insurance.number_other_status * 100) /
									insurance.number_insured,
								variant: 'danger',
							},
							{
								progress:
									(insurance.number_pending * 100) / insurance.number_insured,
								variant: 'primary',
							},
							{
								progress:
									(insurance.number_accepted * 100) / insurance.number_insured,
								variant: 'success',
							},
						]"
						:variant="'success'" />
				</div>
				<div class="w-full inline-flex relative h-10">
					<div v-if="insurance.insurance_type.name === 'Team'" class="w-10 h-10" />
					<img
						v-else
						class="rounded-full w-10 h-10 absolute border border-gray-600"
						:style="`left: ${idx * 24}px`"
						v-for="(url, idx) in insurance.urls"
						:key="url"
						:src="url"
						alt="P" />
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import Button from "@/components/partials/button.vue";
import ChooseNewInsuranceTypeModal from "@/components/coach/modals/chooseNewInsuranceType.vue";
import LoadingBar from "@/components/partials/loadingBar.vue";
import MultipleLoadingBar from "@/components/partials/multipleLoadingBar.vue";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import FileInput from "@/components/partials/inputs/fileInput.vue";
import Loading from "@/components/partials/loading.vue";
import { PencilIcon, ArrowLeftIcon, PlusIcon } from "@heroicons/vue/24/solid";
import { authApi, errorHandling } from "@/services/api";
import toast from "@/toast.js";
import { ref, onMounted } from "vue";
import { useI18n } from "vue-i18n";

const { t } = useI18n({ useScope: "global" });

const props = defineProps({
	teamId: {
		type: String,
		required: true,
	},
});

const insurances = ref([]);
const loading = ref(true);
const loadingUploadPaymentComprovative = ref(false);
const insuranceYear = ref(new Date().getFullYear().toString());
const selectGroupsToSendPaymentComprovative = ref(false);
const groupsToSendPaymentComprovative = ref([]);
const groupsToGetPaymentGuide = ref([]);
const paymentComprovative = ref(null);
const selectInsurancesForPaymentGuide = ref(false);
const loadingDownloadPaymentGuide = ref(false);
const openNewInsuranceModal = ref(false);

onMounted(async () => {
	if (new Date().getMonth() === 11)
		insuranceYear.value = (Number(insuranceYear.value) + 1).toString();
	getInsurances();
});

const getInsurances = async () => {
	try {
		const { data } = await authApi.get(
			`insurances/teams/${props.teamId}?year=${insuranceYear.value}`
		);
		insurances.value = data;
		for (const insurance of insurances.value) {
			insurance.urls = [];
			for (let i = 0; i < insurance.number_insured; i++) {
				if (insurance.profile_pictures.length > i)
					if (insurance.profile_pictures[i] != "None")
						insurance.urls.push(
							`https://kempo-files.fra1.digitaloceanspaces.com/${insurance.profile_pictures[i]}`
						);
					else insurance.urls.push("/defaultUserImage.png");
				else insurance.urls.push("/defaultUserImage.png");
			}
		}
		loading.value = false;
	} catch (e) {
		console.error(e);
		errorHandling(e);
	}
};

const toogleGroupToSendPaymentComprovatives = (id) => {
	const index = groupsToSendPaymentComprovative.value.findIndex((a) => a === id);
	if (index === -1) {
		groupsToSendPaymentComprovative.value.push(id);
	} else {
		groupsToSendPaymentComprovative.value.splice(index, 1);
	}
};
const toogleGroupToGetPaymentGuide = (id) => {
	const index = groupsToGetPaymentGuide.value.findIndex((a) => a === id);
	if (index === -1) {
		groupsToGetPaymentGuide.value.push(id);
	} else {
		groupsToGetPaymentGuide.value.splice(index, 1);
	}
};

const sendPaymentComprovative = async () => {
	if (paymentComprovative.value == null || groupsToSendPaymentComprovative.value.length === 0) {
		toast.error(t("error.insurancePaymentComprovative"));
		return;
	}
	loadingUploadPaymentComprovative.value = true;
	try {
		const formData = new FormData();
		formData.append("sub_team_ids_in", JSON.stringify(groupsToSendPaymentComprovative.value));

		formData.append("file", paymentComprovative.value);
		const response = await authApi.put("insurances/multi/payment-comprovative", formData, {
			headers: { "Content-Type": "multipart/form-data" },
		});
		selectGroupsToSendPaymentComprovative.value = false;
		groupsToSendPaymentComprovative.value = [];
		loadingUploadPaymentComprovative.value = false;
	} catch (e) {
		loadingUploadPaymentComprovative.value = false;
		console.error(e);
		errorHandling(e);
	}
};

const getPaymentGuide = async () => {
	if (groupsToGetPaymentGuide.value.length === 0) {
		toast.error(t("error.insurancePaymentGuide"));
		return;
	}
	loadingDownloadPaymentGuide.value = true;
	try {
		let url = `insurances/get-payment-guide?team_id=${props.teamId}`;
		for (const group of groupsToGetPaymentGuide.value) {
			url += `&sub_team_groups=${group}`;
		}
		const { data } = await authApi.get(url, { responseType: "blob" });

		const pdfUrl = URL.createObjectURL(data);
		const a = document.createElement("a");
		a.download = "payment_guide.pdf";
		a.href = pdfUrl;
		a.target = "_self";
		a.click();

		setTimeout(function () {
			// For Firefox it is necessary to delay revoking the ObjectURL
			a.remove();
			URL.revokeObjectURL(pdfUrl);
		}, 100);

		selectInsurancesForPaymentGuide.value = false;
		groupsToGetPaymentGuide.value = [];
		loadingDownloadPaymentGuide.value = false;
	} catch (e) {
		loadingDownloadPaymentGuide.value = false;
		console.error(e);
		errorHandling(e);
	}
};
</script>
