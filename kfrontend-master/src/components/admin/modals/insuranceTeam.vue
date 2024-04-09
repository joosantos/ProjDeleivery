<template>
	<div>
		<TransitionRoot as="template" :show="open">
			<Dialog as="div" class="fixed z-20 inset-0 overflow-y-auto" @close="emit('close')">
				<div
					class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
					<TransitionChild
						as="template"
						enter="ease-out duration-300"
						enter-from="opacity-0"
						enter-to="opacity-100"
						leave="ease-in duration-200"
						leave-from="opacity-100"
						leave-to="opacity-0">
						<DialogOverlay
							class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" />
					</TransitionChild>

					<!-- This element is to trick the browser into centering the modal contents. -->
					<span
						class="hidden sm:inline-block sm:align-middle sm:h-screen"
						aria-hidden="true"
						>&#8203;</span
					>
					<TransitionChild
						as="template"
						enter="ease-out duration-300"
						enter-from="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95"
						enter-to="opacity-100 translate-y-0 sm:scale-100"
						leave="ease-in duration-200"
						leave-from="opacity-100 translate-y-0 sm:scale-100"
						leave-to="opacity-0 translate-y-4 sm:translate-y-0 sm:scale-95">
						<div
							class="inline-block align-bottom bg-white rounded-lg px-4 pt-5 pb-4 text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-3xl sm:w-full sm:p-6">
							<Loading v-if="loading" :size="10" />
							<FormAthlete
								v-else
								id="insuranceInformationForm"
								:title="t('modalTitle')"
								:subtitle="t('modalSub')"
								:button-save="isEdit ? t('button.edit') : t('button.create')"
								:button-edit="''"
								:can-edit="true"
								:show-loading="showSpinningWheel"
								:show-x="showX"
								@submited="updateInsurance"
								@edit="null">
								<!-- Insured Type Input -->
								<div class="col-span-12 sm:col-span-6">
									<SearchSelect
										:options="insuredTypes"
										:readonly="isEdit"
										:title="t('modalForm.insuredType')"
										:option-selected="stateM.insuredType"
										:error="
											vM$.insuredType.$errors.length == 0
												? ''
												: vM$.insuredType.$errors[0].$message
										"
										@selected="(option) => (stateM.insuredType = option)" />
								</div>
								<!-- Insurance Type Input -->
								<div class="col-span-12 sm:col-span-6">
									<SearchSelect
										:options="insuranceTypes"
										:title="t('modalForm.insuranceType')"
										:option-selected="stateM.insuranceType"
										:error="
											vM$.insuranceType.$errors.length == 0
												? ''
												: vM$.insuranceType.$errors[0].$message
										"
										@selected="(option) => (stateM.insuranceType = option)" />
								</div>
								<!-- Insurance Group Input -->
								<div class="col-span-12">
									<SearchSelect
										:options="insuranceGroups"
										:title="t('modalForm.insuranceGroup')"
										:option-selected="stateM.insuranceGroup"
										:error="
											vM$.insuranceGroup.$errors.length == 0
												? ''
												: vM$.insuranceGroup.$errors[0].$message
										"
										@selected="(option) => (stateM.insuranceGroup = option)" />
								</div>
								<!-- Insurance Start Date Input -->
								<div class="col-span-12 sm:col-span-6">
									<DateInput
										:label="t('modalForm.insuranceStart')"
										:name="'insuranceStart'"
										:option-selected="stateM.insuranceStart"
										:error="
											vM$.insuranceStart.$errors.length == 0
												? ''
												: vM$.insuranceStart.$errors[0].$message
										"
										@value-changed="
											(option) => (stateM.insuranceStart = option)
										" />
								</div>
								<!-- Insurance End Date Input -->
								<div class="col-span-12 sm:col-span-6">
									<DateInput
										:label="t('modalForm.insuranceEnd')"
										:name="'insuranceEnd'"
										:option-selected="stateM.insuranceEnd"
										:error="
											vM$.insuranceEnd.$errors.length == 0
												? ''
												: vM$.insuranceEnd.$errors[0].$message
										"
										@value-changed="
											(option) => (stateM.insuranceEnd = option)
										" />
								</div>
							</FormAthlete>
						</div>
					</TransitionChild>
				</div>
			</Dialog>
		</TransitionRoot>
	</div>
</template>

<script setup>
import Loading from "@/components/partials/loading.vue";
import { Dialog, DialogOverlay, TransitionChild, TransitionRoot } from "@headlessui/vue";
import SearchSelect from "@/components/partials/inputs/searchSelect.vue";
import DateInput from "@/components/partials/inputs/dateInput.vue";
import FormAthlete from "@/components/partials/templates/formAthlete.vue";
import { useI18n } from "vue-i18n";
import { ref, watch } from "vue";
import { authApi, errorHandling, translateDateFromApi } from "@/services/api";
import { required, helpers } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import toast from "@/toast.js";

let { t } = useI18n();

const props = defineProps({
	open: {
		type: Boolean,
		required: true,
	},
	team: {
		type: Object,
		required: true,
	},
	insuranceId: {
		type: String,
		required: false,
		default: "",
	},
});
const emit = defineEmits(["close", "updated"]);

let open = ref(false);
let insurance = ref(null);
let loading = ref(true);
let showSpinningWheel = ref(false);
let showX = ref(false);
let insuredTypes = ref([]);
let insuranceTypes = ref([]);
let insuranceGroups = ref([]);
let initialPromises = [];
const req = helpers.withMessage(t("error.required"), required);
const startDate = helpers.withMessage(
	t("error.startDate"),
	(value) => parseDate(value) < parseDate(stateM.value.insuranceEnd)
);
const endDate = helpers.withMessage(
	t("error.endDate"),
	(value) => parseDate(value) > parseDate(stateM.value.insuranceStart)
);
let stateM = ref({
	insuredType: "",
	insuranceType: "",
	insuranceGroup: "",
	insuranceStart: "",
	insuranceEnd: "",
});

let rulesM = {
	insuredType: {
		required: req,
	},
	insuranceType: {
		required: req,
	},
	insuranceGroup: {},
	insuranceStart: {
		required: req,
		startDate: startDate,
	},
	insuranceEnd: {
		required: req,
		endDate: endDate,
	},
};

let isEdit = ref(false);
let vM$ = useVuelidate(rulesM, stateM, { $scope: "insuranceModal" });

initialPromises.push(
	authApi.get("insured-types").then((response) => {
		insuredTypes.value = response.data;
	})
);
initialPromises.push(
	authApi.get("insurance-types").then((response) => {
		insuranceTypes.value = response.data;
	})
);
initialPromises.push(
	authApi.get("insurance-groups").then((response) => {
		insuranceGroups.value.push({ id: "", name: t("none") });
		insuranceGroups.value.push(...response.data);
	})
);

Promise.all(initialPromises)
	.then(() => {
		loading.value = false;
	})
	.catch((error) => {
		errorHandling(error);
	});

watch(
	() => props.open,
	(after) => {
		open.value = after;
		if (after == false) {
			return;
		}
		if (props.team == null) {
			toast.error(t("error.noTeam"));
			emit("close");
			return;
		}
		console.log(props.team);
		if (props.team.insured_entity_id == null || props.team.insured_entity_id == "") {
			stateM.value.insuredType = "";
		} else {
			stateM.value.insuredType = props.team.insured_entity.insured_type_id;
		}
		isEdit.value = props.insuranceId !== "";
		insurance.value = null;
		stateM.value.insuranceType = "";
		stateM.value.insuranceGroup = "";
		stateM.value.insuranceStart = "";
		stateM.value.insuranceEnd = "";
		showSpinningWheel.value = false;
		showX.value = false;
		vM$.value.$reset();

		if (props.insuranceId != "") getInsurance();
	}
);
watch(
	() => stateM.value.insuranceStart,
	() => {
		let aux = stateM.value.insuranceStart.split("-");
		stateM.value.insuranceEnd = `${aux[0]}-${aux[1]}-${(Number(aux[2]) + 1).toString()}`;
	}
);

function getInsurance() {
	loading.value = true;
	authApi
		.get(`insurances/${props.insuranceId}`)
		.then((response) => {
			insurance.value = response.data;
			stateM.value.insuredType = props.team.insured_entity.insured_type_id;
			stateM.value.insuranceType = response.data.insurance_type_id;
			stateM.value.insuranceGroup = response.data.insurance_group_id;
			stateM.value.insuranceStart = translateDateFromApi(response.data.insurance_start_date);
			stateM.value.insuranceEnd = translateDateFromApi(response.data.insurance_end_date);
			loading.value = false;
		})
		.catch((error) => {
			errorHandling(error);
		});
}

async function updateInsurance() {
	showX.value = false;
	showSpinningWheel.value = true;
	let isFormValid = await vM$.value.$validate();
	if (!isFormValid) {
		showX.value = true;
		showSpinningWheel.value = false;
		return;
	}

	let apiData = {
		insured_type_id: stateM.value.insuredType,
		insurance_type_id: stateM.value.insuranceType,
		insurance_group_id: stateM.value.insuranceGroup,
		insurance_start_date: stateM.value.insuranceStart,
		insurance_end_date: stateM.value.insuranceEnd,
	};

	let promise = isEdit.value
		? authApi.put(`insurances/${props.insuranceId}`, apiData)
		: authApi.post(`teams/${props.team.id}/insurances`, apiData);

	promise
		.then(() => {
			showSpinningWheel.value = false;
			emit("updated");
			emit("close");
		})
		.catch((error) => {
			showSpinningWheel.value = false;
			showX.value = true;
			errorHandling(error);
		});
}

function parseDate(dateString) {
	let aux = dateString.split("-");
	return new Date(aux[2], aux[1] - 1, aux[0]);
}
</script>

<i18n>
{
  "en_GB": {
    "modalForm": {
        "insuredType": "Insured Type",
        "insuranceType": "Insurance Type",
        "insuranceGroup": "Insurance Group",
        "insuranceStart": "Insurance Start Date",
        "insuranceEnd": "Insurance End Date",
    },
    "button": {
        "create": "Create Insurance",
        "edit": "Edit Insurance"
    },
    "error": {
        "required": "Cannot be empty",
        "startDate": "The start date must be before than the end date",
        "endDate": "The end date must be after the start date",
		"noTeam": "No Team to insure"
    },
	"none": "None",
    "modalTitle": "Team's Insurance Information",
    "modalSub": "This information is only available for the admins"
  },
  "pt_PT": {
    "modalForm": {
        "insuredType": "Tipo de Segurado",
        "insuranceType": "Tipo de Seguro",
        "insuranceGroup": "Grupo de Seguro",
        "insuranceStart": "Data de início do Seguro",
        "insuranceEnd": "Data de fim do Seguro",
    },
    "button": {
        "create": "Criar Seguro",
        "edit": "Editar Seguro"
    },
    "error": {
        "required": "Não pode estar vazio",
        "startDate": "A data inicial tem de ser anterior à data final",
        "endDate": "A data final tem de ser posterior à data inicial",
		"noTeam": "Sem Equipa para assegurar"
    },
	"none": "Nenhum",
    "modalTitle": "Informação do Seguro da Equipa",
    "modalSub": "Esta informação é apenas acessível aos Admins"
  },
}
</i18n>
