<template>
	<div>
		<DenyInsuranceRequestModal
			:open="openDenyModalVar"
			:insured-name="
				insurances[insuranceToRefuseIdx] == null
					? ''
					: insurances[insuranceToRefuseIdx].insured_entity.athlete_id
					? insurances[insuranceToRefuseIdx].insured_entity.athlete.name
					: insurances[insuranceToRefuseIdx].insured_entity.team.name
			"
			@close="openDenyModalVar = false"
			@refuse="
				(option) =>
					insuranceToRefuseIdx == -1
						? updateAllSelectedInsuraces(false, option)
						: refuseInsurance(option)
			" />
		<div class="text-2xl font-semibold">
			<p>{{ t("insurances") }}</p>
			<p v-if="props.insuranceGroup && insuranceGroup">
				{{ t("GroupName", { name: insuranceGroup.name }) }}
			</p>
		</div>
		<div v-if="props.insuranceGroup" class="ml-auto max-w-max">
			<Button
				class="max-w-max"
				:message="t('exportAcceptedInsurancesToExcel')"
				:type="'success'"
				:pill="true"
				:icon-left="true"
				:icon="ArrowUpOnSquareIcon"
				:loading="loadingExcel"
				@button-click="exportToExcel" />
		</div>

		<!-- Top Buttons -->
		<div class="inline-flex w-full justify-between mt-4">
			<router-link
				:to="{
					name: 'Insurances',
				}">
				<Button
					class="max-w-max"
					:message="t('returnToInsurancesList')"
					:type="'primary'"
					:pill="true"
					:icon-left="true"
					:icon="ArrowLeftIcon"
					@button-click="null" />
			</router-link>
			<div v-if="!props.insuranceId" class="space-x-4">
				<Button
					class="max-w-max"
					:message="t('acceptAllSelected')"
					:type="'success'"
					:pill="true"
					:loading="loadingAll"
					@button-click="updateAllSelectedInsuraces(true)" />
				<Button
					class="max-w-max"
					:message="t('refuseAllSelected')"
					:type="'danger'"
					:pill="true"
					:loading="loadingAll"
					@button-click="openDenyModal(null)" />
			</div>
		</div>
		<div v-if="!props.insuranceId" class="space-x-4 ml-auto min-w-max max-w-min">
			<Button
				class="max-w-max mt-4"
				:message="t('selectAll')"
				:type="'primary'"
				:pill="true"
				:size="'small'"
				:loading="loadingAll"
				@button-click="selectAll" />
			<Button
				class="max-w-max mt-4"
				:message="t('unselectAll')"
				:type="'primary'"
				:pill="true"
				:size="'small'"
				:loading="loadingAll"
				@button-click="unselectAll" />
		</div>

		<!-- Insurance's List -->
		<Loading v-if="loading" :size="10" />
		<div v-else class="grid grid-cols-1 w-full gap-y-4 mt-4">
			<div
				v-for="insurance of insurances"
				:key="insurance.id"
				:class="[
					'flex flex-col xl:inline-flex xl:flex-row xl:gap-x-8 w-full border rounded-lg px-4 py-2 xl:h-28 gap-y-2 xl:gap-y-0',
					insurance.status === 'pending'
						? 'bg-blue-100 border-blue-300'
						: insurance.status === 'accepted'
						? 'bg-green-100 border-green-300'
						: 'bg-red-100 border-red-300',
				]">
				<!-- Image and name -->
				<div class="min-w-[200px] xl:w-full flex mx-auto xl:mx-0">
					<router-link
						:to="
							insurance.insured_entity.athlete_id
								? {
										name: 'Athlete Details',
										params: { athleteId: insurance.insured_entity.athlete_id },
								  }
								: {
										name: 'Admin Team View',
										params: { teamId: insurance.insured_entity.team_id },
								  }
						"
						target="_blank"
						class="inline-flex space-x-4 w-ful link">
						<img
							class="w-16 h-16 rounded-full my-auto"
							:src="
								insurance.insured_entity?.athlete?.profile_picture_url
									? `https://kempo-files.fra1.digitaloceanspaces.com/${insurance.insured_entity.athlete.profile_picture_url}`
									: '/defaultUserImage.png'
							"
							alt="Profile Picture" />
						<p class="my-auto w-full">
							{{
								insurance.insured_entity.team_id == null
									? insurance.insured_entity.athlete.name
									: insurance.insured_entity.team.name
							}}
						</p>
					</router-link>
				</div>

				<!-- Status -->
				<div
					class="xl:ml-auto xl:min-w-[200px] xl:max-w-[200px] overflow-y-auto w-full text-center xl:text-left">
					<p>
						{{ t("status") }}:
						<span>{{ t(insurance.status) }}</span>
					</p>
					<p v-if="insurance.status !== 'pending' && insurance.status !== 'accepted'">
						{{ insurance.notes }}
					</p>
				</div>

				<!-- Medical Exam -->
				<div class="xl:w-full max-w-[15rem] mx-auto xl:mx-0">
					<div
						v-if="insurance.medical_exam_url && !insurance.editMedicalExam"
						class="min-w-max inline-flex gap-x-2">
						<a
							class="min-w-max link"
							target="_blank"
							:href="
								'https://kempo-files.fra1.cdn.digitaloceanspaces.com/' +
								insurance.medical_exam_url
							">
							{{ t("seeMedicalExam") }}
						</a>
						<PencilIcon
							class="h-6 w-6 p-1 cursor-pointer rounded-full border border-yellow-600 bg-yellow-200 text-yellow-600 hover:bg-yellow-400"
							@click="insurance.editMedicalExam = true" />
					</div>
					<div v-else class="flex flex-col min-w-max">
						<div class="w-full inline-flex gap-x-2">
							<XMarkIcon
								v-if="insurance.medical_exam_url"
								class="h-6 w-6 p-1 cursor-pointer rounded-full border border-red-600 bg-red-200 text-red-600 hover:bg-red-400"
								@click="insurance.editMedicalExam = false" />
							<PlusIcon
								v-else
								class="h-6 w-6 p-1 rounded-lg bg-green-200 border border-green-600 hover:bg-green-400 cursor-pointer" />
							<FileInput
								class="w-56"
								:name="'newMedicalExam'"
								:label="
									t(
										insurance.medical_exam_url
											? 'updateMedicalExam'
											: 'newMedicalExam'
									)
								"
								:error="''"
								@value-changed="(option) => (insurance.newMedicalExam = option)" />
						</div>
						<Button
							class="max-w-max px-8 mx-auto mt-2"
							:message="t('save')"
							:type="'primary'"
							:pill="true"
							:size="'small'"
							:loading="insurance.loadingMedicalExam"
							:disabled="!insurance.newMedicalExam"
							@button-click="updateMedicalExam(insurance.id)" />
					</div>
				</div>

				<!-- Payment Comprovative -->
				<div class="xl:w-full max-w-[15rem] mx-auto xl:mx-0">
					<div
						v-if="
							insurance.payment_comprovative_url && !insurance.editPaymentComprovative
						"
						class="min-w-max inline-flex gap-x-2">
						<a
							class="min-w-max link"
							target="_blank"
							:href="
								'https://kempo-files.fra1.cdn.digitaloceanspaces.com/' +
								insurance.payment_comprovative_url
							">
							{{ t("seePaymentComprovative") }}
						</a>
						<PencilIcon
							class="h-6 w-6 p-1 cursor-pointer rounded-full border border-yellow-600 bg-yellow-200 text-yellow-600 hover:bg-yellow-400"
							@click="insurance.editPaymentComprovative = true" />
					</div>
					<div v-else class="flex flex-col min-w-max">
						<div class="w-full inline-flex gap-x-2">
							<XMarkIcon
								v-if="insurance.payment_comprovative_url"
								class="h-6 w-6 p-1 cursor-pointer rounded-full border border-red-600 bg-red-200 text-red-600 hover:bg-red-400"
								@click="insurance.editPaymentComprovative = false" />
							<PlusIcon
								v-else
								class="h-6 w-6 p-1 rounded-lg bg-green-200 border border-green-600 hover:bg-green-400 cursor-pointer" />
							<FileInput
								class="w-56"
								:name="'newPaymentComprovative'"
								:label="
									t(
										insurance.payment_comprovative_url
											? 'updatePaymentComprovative'
											: 'newPaymentComprovative'
									)
								"
								:error="''"
								@value-changed="
									(option) => (insurance.newPaymentComprovative = option)
								" />
						</div>
						<Button
							class="max-w-max px-8 mx-auto mt-2"
							:message="t('save')"
							:type="'primary'"
							:pill="true"
							:size="'small'"
							:loading="insurance.loadingPaymentComprovative"
							:disabled="!insurance.newPaymentComprovative"
							@button-click="updatePaymentComprovative(insurance.id)" />
					</div>
				</div>

				<!-- Accept or Refuse Buttons -->
				<div class="min-w-max my-auto flex flex-col gap-y-4 w-20 mx-auto">
					<Button
						class="px-8 w-full"
						:message="t('federationRequest.accept')"
						:type="'success'"
						:pill="true"
						:size="'small'"
						:loading="insurance.loadingStatus"
						@button-click="acceptInsurance(insurance.id)" />
					<Button
						class="px-8 w-full"
						:message="t('federationRequest.refuse')"
						:type="'danger'"
						:pill="true"
						:size="'small'"
						:loading="insurance.loadingStatus"
						@button-click="openDenyModal(insurance.id)" />
				</div>

				<!-- Checkbox -->
				<div v-if="!props.insuranceId" class="min-w-max my-auto mx-auto">
					<input
						:id="`insurance-selected-${insurance.id}`"
						v-model="insurance.checked"
						:name="`insurance-selected-${insurance.id}`"
						type="checkbox"
						class="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500" />
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import Button from "@/components/partials/button.vue";
import FileInput from "@/components/partials/inputs/fileInput.vue";
import DenyInsuranceRequestModal from "@/components/admin/modals/denyInsuranceRequest.vue";
import Loading from "@/components/partials/loading.vue";
import { PencilIcon, ArrowLeftIcon, PlusIcon, XMarkIcon } from "@heroicons/vue/24/solid";
import { ArrowUpOnSquareIcon } from "@heroicons/vue/24/outline";
import { authApi, errorHandling } from "@/services/api";
import toast from "@/toast.js";
import { ref, onMounted } from "vue";
import store from "@/store";
import { useI18n } from "vue-i18n";

const { t } = useI18n({ useScope: "global" });

const props = defineProps({
	paymentComprovativeUrl: {
		type: String,
		required: false,
		default: "",
	},
	insuranceGroup: {
		type: String,
		required: false,
		default: "",
	},
	insuranceId: {
		type: String,
		required: false,
		default: "",
	},
});

const insurances = ref([]);
const loading = ref(true);
const openDenyModalVar = ref(false);
const insuranceToRefuseIdx = ref(-1);
const loadingAll = ref(false);
const loadingExcel = ref(false);
const insuranceGroup = ref(null);

onMounted(async () => {
	getInsurances();
});

const getInsurances = async () => {
	try {
		const { data } = await authApi.get(
			`insurances?payment_comprovative_url=${props.paymentComprovativeUrl || ""}&group=${
				props.insuranceGroup || ""
			}&insurance_id=${props.insuranceId || ""}&limit=-1`
		);
		insurances.value = data.results;
		for (let insurance of insurances.value) {
			insurance.newMedicalExam = null;
			insurance.newPaymentComprovative = null;
			insurance.loadingMedicalExam = false;
			insurance.loadingPaymentComprovative = false;
			insurance.editMedicalExam = false;
			insurance.editPaymentComprovative = false;
			insurance.checked = false;
			insurance.loadingStatus = false;
		}
		insuranceGroup.value = insurances.value[0].insurance_group;
		loading.value = false;
	} catch (e) {
		console.error(e);
		errorHandling(e);
	}
};

const selectAll = () => {
	for (let insurance of insurances.value) {
		insurance.checked = true;
	}
};

const unselectAll = () => {
	for (let insurance of insurances.value) {
		insurance.checked = false;
	}
};

const updateMedicalExam = async (insuranceId) => {
	const idx = insurances.value.findIndex((a) => a.id === insuranceId);
	if (idx === -1) return;

	if (insurances.value[idx].newMedicalExam == null) {
		toast.error(t("error.noFile"));
		return;
	}

	insurances.value[idx].loadingMedicalExam = true;
	try {
		const formData = new FormData();
		formData.append("file", insurances.value[idx].newMedicalExam);
		const { data } = await authApi.put(`insurances/${insuranceId}/medical-exam`, formData, {
			headers: { "Content-Type": "multipart/form-data" },
		});
		insurances.value[idx] = data;
		toast.success(t("updated"));
		insurances.value[idx].loadingMedicalExam = false;
	} catch (e) {
		insurances.value[idx].loadingMedicalExam = false;
		console.error(e);
		errorHandling(e);
	}
};

const updatePaymentComprovative = async (insuranceId) => {
	const idx = insurances.value.findIndex((a) => a.id === insuranceId);
	if (idx === -1) return;

	if (insurances.value[idx].newPaymentComprovative == null) {
		toast.error(t("error.noFile"));
		return;
	}

	insurances.value[idx].loadingPaymentComprovative = true;
	try {
		const formData = new FormData();
		formData.append("file", insurances.value[idx].newPaymentComprovative);
		const { data } = await authApi.put(
			`insurances/${insuranceId}/payment-comprovative`,
			formData,
			{
				headers: { "Content-Type": "multipart/form-data" },
			}
		);
		insurances.value[idx] = data;
		toast.success(t("updated"));
		insurances.value[idx].loadingPaymentComprovative = false;
	} catch (e) {
		insurances.value[idx].loadingPaymentComprovative = false;
		console.error(e);
		errorHandling(e);
	}
};

const openDenyModal = (insuranceId) => {
	insuranceToRefuseIdx.value = -1;
	if (insuranceId)
		insuranceToRefuseIdx.value = insurances.value.findIndex((a) => a.id === insuranceId);
	else {
		let showError = true;
		for (let i = 0; i < insurances.value.length; i++) {
			if (insurances.value[i].checked) {
				showError = false;
			}
		}
		if (showError) {
			toast.error(t("error.youMustSelectAtLeastOneInsurance"));
			return;
		}
	}
	openDenyModalVar.value = true;
};

const acceptInsurance = async (insuranceId) => {
	const idx = insurances.value.findIndex((a) => a.id === insuranceId);
	insurances.value[idx].loadingStatus = true;
	try {
		const { data } = await authApi.put(`insurances/${insuranceId}`, {
			status: "accepted",
		});
		insurances.value[idx].status = "accepted";
	} catch (e) {
		errorHandling(e);
	} finally {
		insurances.value[idx].loadingStatus = false;
	}
};

const refuseInsurance = async (refuseMotive) => {
	insurances.value[insuranceToRefuseIdx.value].loadingStatus = true;
	openDenyModalVar.value = false;
	try {
		const { data } = await authApi.put(
			`insurances/${insurances.value[insuranceToRefuseIdx.value].id}`,
			{
				status: "denied",
				notes: refuseMotive,
			}
		);
		insurances.value[insuranceToRefuseIdx.value].status = "denied";
		insurances.value[insuranceToRefuseIdx.value].notes = refuseMotive;
	} catch (e) {
		errorHandling(e);
	} finally {
		insurances.value[insuranceToRefuseIdx.value].loadingStatus = false;
	}
};

const updateAllSelectedInsuraces = async (approve, refuseMotive = null) => {
	const idxs = [];
	const ids = [];
	loadingAll.value = true;
	for (let i = 0; i < insurances.value.length; i++) {
		if (insurances.value[i].checked) {
			idxs.push(i);
			ids.push(insurances.value[i].id);
			insurances.value[i].loadingStatus = true;
		}
	}
	if (!idxs.length) {
		loadingAll.value = false;
		toast.error(t("error.youMustSelectAtLeastOneInsurance"));
		return;
	}
	openDenyModalVar.value = false;
	try {
		await authApi.put("insurances/multi/status-update", {
			ids: ids,
			status: approve ? "accepted" : "denied",
			notes: refuseMotive,
		});
		for (let i = 0; i < insurances.value.length; i++) {
			insurances.value[i].checked = false;
			insurances.value[i].status = approve ? "accepted" : "denied";
			insurances.value[i].notes = refuseMotive;
			insurances.value[i].loadingStatus = false;
			loadingAll.value = false;
		}
	} catch (e) {
		errorHandling(e);
		for (let i = 0; i < insurances.value.length; i++) {
			insurances.value[i].checked = false;
			insurances.value[i].loadingStatus = false;
			loadingAll.value = false;
		}
	}
};

const exportToExcel = async () => {
	loadingExcel.value = true;
	try {
		const { data } = await authApi.get(
			`insurances/get-excel?insurance_group_id=${props.insuranceGroup}`,
			{
				responseType: "blob",
			}
		);
		const docURL = URL.createObjectURL(data);
		const a = document.createElement("a");
		a.download = `${insuranceGroup.value.name}_federacoes.xlsx`;
		a.href = docURL;
		a.target = "_self";
		a.click();

		setTimeout(function () {
			// For Firefox it is necessary to delay revoking the ObjectURL
			a.remove();
			URL.revokeObjectURL(docURL);
		}, 100);
	} catch (e) {
		errorHandling(e);
	} finally {
		loadingExcel.value = false;
	}
};
</script>
