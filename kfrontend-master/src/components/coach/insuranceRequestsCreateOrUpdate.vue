<template>
	<div>
		<router-link
			:to="{ name: 'Insurance Requests', params: { teamId: props.teamId } }"
			class="ml-4">
			<Button
				class="max-w-max mt-4"
				:message="t('returnToInsurancesList')"
				:type="'primary'"
				:pill="true"
				:iconLeft="true"
				:icon="ArrowLeftIcon"
				@button-click="null" />
		</router-link>
		<div
			:class="[
				'grid grid-cols-1',
				variant === 'team' ? 'lg:grid-cols-1' : 'lg:grid-cols-2 ',
			]">
			<div v-if="variant !== 'team'" class="bg-gray-50 p-4 rounded-lg">
				<FormTemplate
					:loading="athletesLoading"
					@clear-form="resetForm"
					@submit-form="searchAthletes">
					<div class="inline-flex space-x-4 mx-auto">
						<CustomInput
							:type="'text'"
							:mask="'#####'"
							:name="'federationNumber'"
							:label="t('forms.federationNumber')"
							:option-selected="formInputs.fedNum"
							:error="''"
							@value-changed="(option) => (formInputs.fedNum = option)" />
						<CustomInput
							:type="'text'"
							:name="'name'"
							:label="t('forms.athleteName')"
							:option-selected="formInputs.name"
							:error="''"
							@value-changed="(option) => (formInputs.name = option)" />
						<CustomInput
							:type="'text'"
							:mask="'###'"
							:name="'age'"
							:label="t('forms.athleteAge')"
							:option-selected="formInputs.age"
							:error="''"
							@value-changed="(option) => (formInputs.age = option)" />
					</div>
				</FormTemplate>

				<div>
					<div class="grid grid-cols-4 gap-x-4 gap-y-2 mt-4">
						<div
							v-for="athlete of athletes"
							:key="athlete.id"
							:class="[
								'px-4 py-2 cursor-pointer',
								athletesToInsure.findIndex(
									(a) => a === athlete.insured_entity_id
								) === -1
									? 'bg-blue-100 border border-blue-300 rounded-lg hover:bg-blue-200'
									: 'bg-indigo-300 border border-indigo-500 rounded-lg hover:bg-indigo-400',
							]"
							@click="toogleAthlete(athlete.insured_entity_id)">
							<div class="inline-flex space-x-2">
								<img
									class="w-10 h-10 rounded-full"
									:src="
										athlete.profile_picture_url
											? `https://kempo-files.fra1.digitaloceanspaces.com/${athlete.profile_picture_url}`
											: '/defaultUserImage.png'
									"
									:alt="`Profile picture for ${athlete.name}`" />
								<p class="">
									{{ athlete.name }}
								</p>
							</div>
						</div>
					</div>
					<div class="mx-auto mt-4 max-w-max">
						<Pagination
							:pages="Math.ceil(numberAthletes / limit)"
							:current="currentPage"
							@page-change="changePage" />
					</div>
				</div>
			</div>

			<div class="bg-gray-50 p-4 rounded-lg">
				<Loading v-if="initialLoading" :size="10"></Loading>
				<FormTemplate
					v-else
					button-text="requestInsurance"
					:loading="insuranceButton === 'loading'"
					:show-check="insuranceButton === 'check'"
					:show-x="insuranceButton === 'x'"
					@clear-form="resetFormInsurance"
					@submit-form="props.insuranceId ? updateInsurance() : createInsurance()">
					<div class="grid xl:grid-cols-6 col-span-2 gap-x-4 gap-y-2 w-full">
						<p v-if="variant === 'team'" class="col-span-full">
							{{ t("requestInsuranceForTeam") }}
						</p>
						<p v-else class="col-span-full">
							{{
								t(
									"numberAthletesToInsure",
									{ number: athletesToInsure.length },
									athletesToInsure.length
								)
							}}
						</p>
						<p v-if="variant !== 'contract'" class="col-span-full">
							{{
								t("price", {
									price:
										athletesToInsure.length *
										(insuranceTypes.find(
											(a) => a.id === formInsurance.insuranceType
										)?.fee || 0),
								})
							}}
						</p>
						<DateInput
							class="xl:col-start-2 col-span-4"
							:label="t('forms.startDate')"
							:name="'startDate'"
							:option-selected="formInsurance.startDate"
							:error="''"
							@value-changed="(option) => (formInsurance.startDate = option)" />
						<SearchSelect
							class="xl:col-start-2 col-span-4"
							:title="t('forms.insuranceType')"
							:options="insuranceTypes"
							:option-selected="formInsurance.insuranceType"
							:readonly="variant === 'team' || variant === 'contract'"
							:error="''"
							@selected="(option) => (formInsurance.insuranceType = option)" />
						<div v-if="props.insuranceId" class="xl:col-start-2 col-span-4">
							<div
								v-if="!editContract"
								class="inline-flex justify-center w-full gap-x-2 text-center mt-2 mb-4">
								<a
									class="min-w-max link"
									target="_blank"
									:href="
										'https://kempo-files.fra1.cdn.digitaloceanspaces.com/' +
										contractUrl
									">
									{{ t("seeContract") }}
								</a>
								<PencilIcon
									class="h-6 w-6 p-1 cursor-pointer rounded-full border border-yellow-600 bg-yellow-200 text-yellow-600 hover:bg-yellow-400"
									@click="editContract = true" />
							</div>
							<div v-else class="flex flex-col xl:col-start-2 col-span-4">
								<div class="max-w-max inline-flex gap-x-2 mx-auto">
									<XMarkIcon
										v-if="contractUrl"
										class="h-6 w-6 p-1 cursor-pointer rounded-full border border-red-600 bg-red-200 text-red-600 hover:bg-red-400"
										@click="editContract = false" />
									<PlusIcon
										v-else
										class="h-6 w-6 p-1 rounded-lg bg-green-200 border border-green-600 hover:bg-green-400 cursor-pointer" />
									<FileInput
										:name="'newMedicalExam'"
										:label="t('updateContract')"
										:error="''"
										@value-changed="
											(option) => (formInsurance.contract = option)
										" />
								</div>
							</div>
						</div>
						<FileInput
							v-else-if="variant === 'contract'"
							class="xl:col-start-2 col-span-4"
							:name="'contract'"
							:label="t('insuranceContract')"
							:error="''"
							@value-changed="(option) => (formInsurance.contract = option)" />
					</div>
				</FormTemplate>
			</div>
		</div>
	</div>
</template>

<script setup>
import Pagination from "@/components/partials/pagination/pagination.vue";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import FileInput from "@/components/partials/inputs/fileInput.vue";
import Button from "@/components/partials/button.vue";
import SearchSelect from "@/components/partials/inputs/searchSelect.vue";
import DateInput from "@/components/partials/inputs/dateInput.vue";
import FormTemplate from "@/components/partials/inputs/formTemplate.vue";
import Loading from "@/components/partials/loading.vue";
import { authApi, errorHandling, translateDateFromApi } from "@/services/api";
import { PencilIcon, ArrowLeftIcon, PlusIcon, XMarkIcon } from "@heroicons/vue/24/solid";
import { ref, onMounted } from "vue";
import router from "@/router";
import { useI18n } from "vue-i18n";

const { t } = useI18n({ useScope: "global" });

const props = defineProps({
	teamId: {
		type: String,
		required: true,
	},
	insuranceId: {
		type: String,
		required: false,
		default: "",
	},
	variant: {
		type: String,
		required: false,
		default: "",
	},
});

const formInputs = ref({
	fedNum: "",
	name: "",
	age: "",
});

const formInsurance = ref({
	startDate: "",
	endDate: "",
	insuranceType: "",
	contract: null,
});

const athletesToInsure = ref([]);
const athletes = ref([]);
const numberAthletes = ref(0);
const limit = 20;
const currentPage = ref(1);
const initialLoading = ref(true);
const athletesLoading = ref(true);
const insuranceButton = ref("none");
const insuranceTypes = ref([]);
const originalInsurances = ref([]);
const contractUrl = ref("");
const editContract = ref(false);
const variant = ref(props.variant || "individuals");

onMounted(async () => {
	const urlParams = new URLSearchParams();
	formInputs.value.fedNum = urlParams.get("federation-number") || "";
	formInputs.value.name = urlParams.get("name") || "";
	formInputs.value.age = urlParams.get("age") || "";
	searchAthletes();
	try {
		const { data } = await authApi.get("insurance-types");
		insuranceTypes.value = data;

		if (props.insuranceId != "") {
			const { data } = await authApi.get(
				`insurances?sub_team_group=${props.insuranceId}&limit=-1`
			);
			originalInsurances.value = data.results;
			formInsurance.value.startDate =
				translateDateFromApi(originalInsurances.value[0].start_date) || "";
			formInsurance.value.endDate =
				translateDateFromApi(originalInsurances.value[0].end_date) || "";
			formInsurance.value.insuranceType = originalInsurances.value[0].insurance_type_id;
			if (originalInsurances.value[0].insurance_type.name === "Team") {
				variant.value = "team";
			} else if (originalInsurances.value[0].insurance_type.name === "Contract") {
				variant.value = "contract";
				contractUrl.value = originalInsurances.value[0].contract_url;
			}
			for (const insurance of originalInsurances.value) {
				athletesToInsure.value.push(insurance.insured_entity_id);
			}
		}
		if (variant.value === "team") {
			formInsurance.value.insuranceType = insuranceTypes.value.find(
				(a) => a.name === "Team"
			)?.id;
			if (props.insuranceId == "") {
				const { data } = await authApi.get(`teams/${props.teamId}`);
				athletesToInsure.value.push(data.insured_entity_id);
			}
		} else {
			let index = insuranceTypes.value.findIndex((a) => a.name === "Team");
			insuranceTypes.value.splice(index, 1);
			if (variant.value === "contract") {
				formInsurance.value.insuranceType = insuranceTypes.value.find(
					(a) => a.name === "Contract"
				)?.id;
			} else {
				index = insuranceTypes.value.findIndex((a) => a.name === "Contract");
				insuranceTypes.value.splice(index, 1);
			}
		}
		initialLoading.value = false;
	} catch (e) {
		errorHandling(e);
	}
});

const resetForm = () => {
	formInputs.value.fedNum = "";
	formInputs.value.name = "";
	formInputs.value.age = "";
	formInputs.value.contract = null;
	searchAthletes();
};

const searchAthletes = async () => {
	athletesLoading.value = true;
	try {
		const { data } = await authApi.get(getApiUrl());
		numberAthletes.value = data.n_results;
		athletes.value = data.results;
		updatePageUrl();
		athletesLoading.value = false;
	} catch (e) {
		athletesLoading.value = false;
		errorHandling(e);
		console.error(e);
	}
};

const getApiUrl = () => {
	if (currentPage.value < 1) currentPage.value = 1;
	let url = `athletes?teams=${[props.teamId]}&limit=${limit}&skip=${
		(currentPage.value - 1) * limit
	}`;
	if (formInputs.value.fedNum) {
		url += `&federation_number=${formInputs.value.fedNum}`;
		return url;
	}
	if (formInputs.value.name) url += `&name=${formInputs.value.name}`;
	if (formInputs.value.age) url += `&age=${formInputs.value.age}`;
	return url;
};

const updatePageUrl = () => {
	const urlParams = new URLSearchParams();
	if (formInputs.value.fedNum) urlParams.set("federation-number", formInputs.value.fedNum);
	if (formInputs.value.name) urlParams.set("name", formInputs.value.name);
	if (formInputs.value.age) urlParams.set("age", formInputs.value.age);
	history.replaceState(null, null, `?${urlParams.toString()}`);
};

const changePage = (page) => {
	currentPage.value = page;
	searchAthletes();
};

const toogleAthlete = (id) => {
	const index = athletesToInsure.value.findIndex((a) => a === id);
	if (index === -1) {
		athletesToInsure.value.push(id);
	} else {
		athletesToInsure.value.splice(index, 1);
	}
};

const resetFormInsurance = () => {
	formInsurance.value.startDate = "";
	formInsurance.value.endDate = "";
	formInsurance.value.insuranceType = "";
};

const createInsurance = async () => {
	insuranceButton.value = "loading";
	try {
		const sub_team_group = crypto.randomUUID();
		await authApi.post("insurances/multi", {
			start_date: formInsurance.value.startDate,
			insurance_type_id: formInsurance.value.insuranceType,
			insured_entities_ids: athletesToInsure.value,
			sub_team_group: sub_team_group,
		});
		if (variant.value === "contract") {
			const formData = new FormData();
			formData.append("file", formInsurance.value.contract);
			await authApi.put(`insurances/${sub_team_group}/contract`, formData, {
				headers: { "Content-Type": "multipart/form-data" },
			});
		}
		insuranceButton.value = "check";
		setTimeout(() => {
			router.push({ name: "Insurance Requests", params: { teamId: props.teamId } });
		}, 1000);
	} catch (e) {
		insuranceButton.value = "x";
		console.error(e);
		errorHandling(e);
	}
};

const updateInsurance = async () => {
	insuranceButton.value = "loading";
	try {
		await authApi.put(`insurances/multi/${props.insuranceId}`, {
			start_date: formInsurance.value.startDate,
			insurance_type_id: formInsurance.value.insuranceType,
			insured_entities_ids: athletesToInsure.value,
		});
		if (variant.value === "contract") {
			const formData = new FormData();
			formData.append("file", formInsurance.value.contract);
			await authApi.put(`insurances/${props.insuranceId}/contract`, formData, {
				headers: { "Content-Type": "multipart/form-data" },
			});
		}
		insuranceButton.value = "check";
		setTimeout(() => {
			router.push({ name: "Insurance Requests", params: { teamId: props.teamId } });
		}, 1000);
	} catch (e) {
		insuranceButton.value = "x";
		console.error(e);
		errorHandling(e);
	}
};
</script>
