<template>
	<div>
		<p class="text-2xl font-semibold">Insurances</p>
		<div class="inline-flex w-full justify-between">
			<router-link
				:to="{
					name: 'Insurance Requests',
					params: { teamId: props.teamId },
				}">
				<Button
					class="max-w-max mt-4"
					:message="t('returnToInsurancesList')"
					:type="'primary'"
					:pill="true"
					:icon-left="true"
					:icon="ArrowLeftIcon"
					@button-click="null" />
			</router-link>
			<router-link
				v-if="insurances.length"
				:to="{
					name: 'Insurance Requests Update',
					params: { teamId: props.teamId, insuranceId: insurances[0].sub_team_group },
				}">
				<Button
					class="max-w-max"
					:message="t('editInsuranceRequest')"
					:type="'warning'"
					:pill="true"
					:icon-left="true"
					:icon="PencilIcon"
					@button-click="() => (selectGroupsToSendPaymentComprovative = true)" />
			</router-link>
		</div>
		<Loading v-if="loading" :size="10" />
		<div v-else class="grid grid-cols-1 w-full gap-y-4 mt-4">
			<div
				v-for="insurance of insurances"
				:key="insurance.id"
				:class="[
					'inline-flex gap-x-8 w-full border rounded-lg px-4 py-2',
					insurance.status === 'pending'
						? 'bg-blue-100 border-blue-300'
						: insurance.status === 'accepted'
						? 'bg-green-100 border-green-300'
						: 'bg-red-100 border-red-300',
				]">
				<!-- Insured's name and image -->
				<div class="inline-flex space-x-4">
					<img
						v-if="insurance.insurance_type.name !== 'Team'"
						class="w-10 h-10 rounded-full"
						:src="
							insurance.insured_entity.athlete.profile_picture_url
								? `https://kempo-files.fra1.digitaloceanspaces.com/${insurance.insured_entity.athlete.profile_picture_url}`
								: '/defaultUserImage.png'
						"
						alt="Profile Picture" />
					<p class="min-w-max">
						{{
							insurance.insurance_type.name === "Team"
								? insurance.insured_entity.team.name
								: insurance.insured_entity.athlete.name
						}}
					</p>
				</div>
				<div class="w-full" />

				<!-- Insurance's Status -->
				<div class="min-w-max">
					<p>
						{{ t("status") }}:
						<span>{{ t(insurance.status) }}</span>
					</p>
					<p v-if="insurance.status !== 'pending' && insurance.status !== 'accepted'">
						{{ insurance.notes }}
					</p>
				</div>

				<!-- Coach's Certificate -->
				<div v-if="insurance.insurance_type.name === 'Coach'" class="min-w-max">
					<div
						v-if="insurance.coach_certificate_url && !insurance.editCoachCertificate"
						class="min-w-max inline-flex gap-x-2">
						<a
							class="min-w-max link"
							target="_blank"
							:href="
								'https://kempo-files.fra1.cdn.digitaloceanspaces.com/' +
								insurance.coach_certificate_url
							">
							{{ t("seeCoachCertificate") }}
						</a>
						<PencilIcon
							class="h-6 w-6 p-1 cursor-pointer rounded-full border border-yellow-600 bg-yellow-200 text-yellow-600 hover:bg-yellow-400"
							@click="insurance.editCoachCertificate = true" />
					</div>
					<div v-else class="flex flex-col min-w-max">
						<div class="w-full inline-flex gap-x-2">
							<XMarkIcon
								v-if="insurance.coach_certificate_url"
								class="h-6 w-6 p-1 cursor-pointer rounded-full border border-red-600 bg-red-200 text-red-600 hover:bg-red-400"
								@click="insurance.editCoachCertificate = false" />
							<PlusIcon
								v-else
								class="h-6 w-6 p-1 rounded-lg bg-green-200 border border-green-600 hover:bg-green-400 cursor-pointer" />
							<FileInput
								:name="'newCoachCertificate'"
								:label="
									t(
										insurance.coach_certificate_url
											? 'updateCoachCertificate'
											: 'newCoachCertificate'
									)
								"
								:error="''"
								@value-changed="
									(option) => (insurance.newCoachCertificate = option)
								" />
						</div>
						<Button
							class="max-w-max px-8 mx-auto mt-2"
							:message="t('save')"
							:type="'primary'"
							:pill="true"
							:size="'small'"
							:loading="insurance.loadingCoachCertificate"
							:disabled="!insurance.newCoachCertificate"
							@button-click="updateCoachCertificate(insurance.id)" />
					</div>
				</div>

				<!-- Insurance's Medical Exam -->
				<div v-if="insurance.insurance_type.name !== 'Team'" class="min-w-max">
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

				<!-- Insurance's Payment Comprovative -->
				<div class="min-w-max">
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
			</div>
		</div>
	</div>
</template>

<script setup>
import Button from "@/components/partials/button.vue";
import FileInput from "@/components/partials/inputs/fileInput.vue";
import Loading from "@/components/partials/loading.vue";
import { PencilIcon, ArrowLeftIcon, PlusIcon, XMarkIcon } from "@heroicons/vue/24/solid";
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
	subTeamGroup: {
		type: String,
		required: true,
	},
});

const insurances = ref([]);
const loading = ref(true);

onMounted(async () => {
	getInsurances();
});

const getInsurances = async () => {
	try {
		const { data } = await authApi.get(
			`insurances?sub_team_group=${props.subTeamGroup}&limit=-1`
		);
		insurances.value = data.results;
		for (let insurance of insurances.value) {
			insurance.editMedicalExam = false;
			insurance.newMedicalExam = null;
			insurance.loadingMedicalExam = false;
			insurance.editPaymentComprovative = false;
			insurance.newPaymentComprovative = null;
			insurance.loadingPaymentComprovative = false;
			insurance.editCoachCertificate = false;
			insurance.newCoachCertificate = null;
			insurance.loadingCoachCertificate = false;
		}
		loading.value = false;
	} catch (e) {
		console.error(e);
		errorHandling(e);
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

const updateCoachCertificate = async (insuranceId) => {
	const idx = insurances.value.findIndex((a) => a.id === insuranceId);
	if (idx === -1) return;

	if (insurances.value[idx].newCoachCertificate == null) {
		toast.error(t("error.noFile"));
		return;
	}

	insurances.value[idx].loadingCoachCertificate = true;
	try {
		const formData = new FormData();
		formData.append("file", insurances.value[idx].newCoachCertificate);
		const { data } = await authApi.put(
			`insurances/${insuranceId}/coach-certificate`,
			formData,
			{
				headers: { "Content-Type": "multipart/form-data" },
			}
		);
		insurances.value[idx] = data;
		toast.success(t("updated"));
	} catch (e) {
		console.error(e);
		errorHandling(e);
	} finally {
		insurances.value[idx].loadingCoachCertificate = false;
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
</script>
