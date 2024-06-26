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
							<form v-else class="space-y-4" @submit.prevent="updateInsuranceType">
								<p class="text-xl font-medium text-center">
									{{ t("titleInsurance") }}
								</p>
								<!-- Name Input -->
								<div class="col-span-12 sm:col-span-6">
									<CustomInput
										:type="'text'"
										:name="'name'"
										:label="t('modalForm.name')"
										:option-selected="state.name"
										:error="
											v$.name.$errors.length == 0
												? ''
												: v$.name.$errors[0].$message
										"
										@value-changed="(option) => (state.name = option)" />
								</div>
								<!-- Description Input -->
								<div class="col-span-12 sm:col-span-6">
									<CustomInput
										:type="'text'"
										:name="'description'"
										:label="t('modalForm.description')"
										:option-selected="state.description"
										:error="
											v$.description.$errors.length == 0
												? ''
												: v$.description.$errors[0].$message
										"
										@value-changed="(option) => (state.description = option)" />
								</div>
								<!-- Fee Input -->
								<div class="col-span-12 sm:col-span-6">
									<CustomInput
										:type="'text'"
										:name="'fee'"
										:label="t('modalForm.fee')"
										:option-selected="state.fee.toString()"
										:error="
											v$.fee.$errors.length == 0
												? ''
												: v$.fee.$errors[0].$message
										"
										@value-changed="(option) => (state.fee = option)" />
								</div>
								<div class="mt-4">
									<Button
										:message="
											isEdit
												? t('buttonInsurance.edit')
												: t('buttonInsurance.create')
										"
										type="primary"
										:submit="true"
										:loading="showSpinningWheel"
										:show-x="showX"
										:pill="true"
										@button-click="null" />
								</div>
							</form>
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
import CustomInput from "@/components/partials/inputs/customInput.vue";
import Button from "@/components/partials/button.vue";
import { useI18n } from "vue-i18n";
import { ref, watch } from "vue";
import { authApi, errorHandling } from "@/services/api";
import { required, helpers, numeric } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";

let { t } = useI18n();

const props = defineProps({
	open: {
		type: Boolean,
		required: true,
	},
	insuranceTypeId: {
		type: String,
		required: false,
		default: "",
	},
});
const emit = defineEmits(["close", "updated"]);

let open = ref(false);
let insuranceType = ref(null);
let loading = ref(true);
let showSpinningWheel = ref(false);
let showX = ref(false);

const req = helpers.withMessage(t("error.required"), required);
const num = helpers.withMessage(t("error.numeric"), numeric);
let state = ref({
	name: "",
	description: "",
	fee: 0,
});

let rules = {
	name: {
		required: req,
	},
	description: {
		required: req,
	},
	fee: {
		required: req,
		num: num,
	},
};

let isEdit = ref(false);
let v$ = useVuelidate(rules, state);

watch(
	() => props.open,
	(after) => {
		open.value = after;
		if (after == false) {
			return;
		}
		loading.value = true;
		isEdit.value = props.insuranceTypeId !== "";
		insuranceType.value = null;
		state.value.name = "";
		state.value.description = "";
		state.value.fee = 0;
		showX.value = false;
		showSpinningWheel.value = false;
		v$.value.$reset();

		if (props.insuranceTypeId != "") getInsuranceType();
		else loading.value = false;
	}
);

function getInsuranceType() {
	loading.value = true;
	authApi
		.get(`insurance-types/${props.insuranceTypeId}`)
		.then((response) => {
			insuranceType.value = response.data;
			state.value.name = response.data.name;
			state.value.description = response.data.description;
			state.value.fee = response.data.fee;
			loading.value = false;
		})
		.catch((error) => {
			errorHandling(error);
		});
}

async function updateInsuranceType() {
	state.value.fee = Number(state.value.fee.toString().replace(",", "."));
	showX.value = false;
	showSpinningWheel.value = true;
	let isFormValid = await v$.value.$validate();
	if (!isFormValid) {
		showX.value = true;
		showSpinningWheel.value = false;
		return;
	}

	let apiData = {
		name: state.value.name,
		description: state.value.description,
		fee: state.value.fee,
	};

	let promise = isEdit.value
		? authApi.put(`insurance-types/${props.insuranceTypeId}`, apiData)
		: authApi.post(`insurance-types`, apiData);

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
</script>

<i18n>
{
    "en_GB": {
        "modalForm": {
            "name": "Name",
            "description": "Description",
            "fee": "Fee",
        },
        "buttonInsurance": {
            "create": "Create Insurance Type",
            "edit": "Edit Insurance Type"
        },
        "error": {
            "required": "Cannot be empty",
            "numeric": "Must be a number"
        },
		"titleInsurance": "Insurance Type"
    },
    "pt_PT": {
        "modalForm": {
            "name": "Nome",
            "description": "Descrição",
            "fee": "Taxa",
        },
        "buttonInsurance": {
            "create": "Criar Tipo de Seguro",
            "edit": "Editar Tipo de Seguro"
        },
        "error": {
            "required": "Não pode estar vazio",
            "numeric": "Tem de ser um número"
        },
		"titleInsurance": "Tipo de Seguro"
    },
}
</i18n>
