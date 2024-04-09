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
							<div v-else>
								<p class="text-xl font-semibold text-center mb-4">
									{{ newTeam ? t("new") : t("updateTeam") }}
								</p>
								<form class="space-y-8">
									<CustomInput
										:label="t('name')"
										type="text"
										:name="'name'"
										:option-selected="state.name"
										:error="
											errorName == ''
												? v$.name.$errors.length == 0
													? ''
													: v$.name.$errors[0].$message
												: errorName
										"
										@value-changed="(option) => (state.name = option)" />
									<CustomInput
										:label="t('abbreviation')"
										type="text"
										mask="AAAAAAAA"
										:name="'abbreviation'"
										:option-selected="state.abbreviation"
										:error="
											errorAbbreviation == ''
												? v$.abbreviation.$errors.length == 0
													? ''
													: v$.abbreviation.$errors[0].$message
												: errorAbbreviation
										"
										@value-changed="
											(option) => (state.abbreviation = option)
										" />
									<CustomInput
										:label="t('association')"
										type="text"
										:name="'association'"
										:option-selected="state.association"
										:error="
											errorAbbreviation == ''
												? v$.association.$errors.length == 0
													? ''
													: v$.association.$errors[0].$message
												: errorAbbreviation
										"
										@value-changed="(option) => (state.association = option)" />
								</form>
								<div class="relative w-60 left-1/2 -translate-x-1/2 mt-20">
									<Button
										:loading="showSpinningWheel"
										:show-x="showX"
										:show-check="showCheck"
										:message="newTeam ? t('create') : t('update')"
										type="primary"
										@button-click="createTeam" />
								</div>
							</div>
						</div>
					</TransitionChild>
				</div>
			</Dialog>
		</TransitionRoot>
	</div>
</template>

<script setup>
import Loading from "@/components/partials/loading.vue";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import Button from "@/components/partials/button.vue";
import { Dialog, DialogOverlay, TransitionChild, TransitionRoot } from "@headlessui/vue";
import { ref, watch } from "vue";
import { authApi } from "@/services/api";
import { required, helpers, maxLength } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";
import toast from "@/toast.js";
import { useI18n } from "vue-i18n";

let { t } = useI18n();

const props = defineProps({
	open: {
		type: Boolean,
		required: true,
	},
	teamId: {
		type: String,
		required: false,
		default: "",
	},
});
const emit = defineEmits(["close", "created", "updated"]);

const req = helpers.withMessage(t("error.required"), required);
const maxLen = helpers.withMessage(t("error.maxLen", { count: 255 }), maxLength(255));
const maxLenAbr = helpers.withMessage(t("error.maxLen", { count: 8 }), maxLength(8));

let state = ref({
	name: "",
	abbreviation: "",
	association: "",
});

let rules = {
	name: {
		required: req,
		max: maxLen,
	},
	abbreviation: {
		required: req,
		max: maxLenAbr,
	},
	association: {
		required: req,
		max: maxLen,
	},
};

let open = ref(false);
let v$ = useVuelidate(rules, state);
let showSpinningWheel = ref(false);
let loading = ref(true);
let showCheck = ref(false);
let showX = ref(false);
let newTeam = ref(true);
let errorName = ref("");
let errorAbbreviation = ref("");

watch(
	() => state.value.name,
	() => {
		errorName.value = "";
	}
);
watch(
	() => state.value.abbreviation,
	() => {
		errorAbbreviation.value = "";
	}
);
watch(
	() => props.open,
	(after) => {
		open.value = after;
		if (after) {
			loading.value = true;
			newTeam.value = props.teamId == "";
			showCheck.value = false;
			showX.value = false;
			showSpinningWheel.value = false;
			state.value.name = "";
			state.value.abbreviation = "";
			state.value.association = "";
			errorName.value = "";
			errorAbbreviation.value = "";
			v$.value.$reset();
			if (!newTeam.value) {
				authApi
					.get(`teams/${props.teamId}`)
					.then((response) => {
						if (response.data == null) {
							toast.error("erros.team");
							emit("close");
							return;
						}
						state.value.name = response.data.name;
						state.value.abbreviation = response.data.abbreviation;
						state.value.association = response.data.association;
						loading.value = false;
					})
					.catch(() => {
						toast.error("erros.team");
						emit("close");
					});
			} else {
				loading.value = false;
			}
		}
	}
);

async function createTeam() {
	showX.value = false;
	showCheck.value = false;
	showSpinningWheel.value = true;

	let isFormValid = await v$.value.$validate();
	if (!isFormValid) {
		showX.value = true;
		showSpinningWheel.value = false;
		return;
	}
	let promisse = newTeam.value
		? authApi.post("teams", {
				name: state.value.name,
				abbreviation: state.value.abbreviation,
				association: state.value.association,
		  })
		: authApi.put(`teams/${props.teamId}`, {
				name: state.value.name,
				abbreviation: state.value.abbreviation,
				association: state.value.association,
		  });
	promisse
		.then(() => {
			showSpinningWheel.value = false;
			showCheck.value = true;
			if (newTeam.value) {
				emit("created");
			} else {
				emit("updated");
			}
			emit("close");
		})
		.catch((error) => {
			let details = error.response.data.detail;
			for (let detail in details) {
				if (details[detail] == "The team name must be unique") {
					errorName.value = t("error.name");
					continue;
				}
				if (details[detail] == "The team abbreviation must be unique") {
					errorAbbreviation.value = t("error.abbreviation");
					continue;
				}
			}
			showSpinningWheel.value = false;
			showX.value = true;
			toast.error(newTeam.value ? t("error.create") : t("error.update"));
		});
}
</script>

<i18n>
{
  "en_GB": {
	"name": "Name",
	"abbreviation": "Abbreviation (max 8 letters)",
	"association": "Association",
	"team": "Team",
	"new": "Create a new Team",
	"updateTeam": "Update Team",
	"create": "Create",
	"update": "Update",
    "error": {
        "required": "Cannot be empty",
		"maxLen": "The max length is {count} characters",
		"team": "Couldn't get the team",
		"create": "Couldn't create the team",
		"update": "Couldn't update the team",
		"name": "Already exists a team with this name",
		"abbreviation": "Already exists a team with this abbreviation",
    }
  },
  "pt_PT": {
	"name": "Nome",
	"abbreviation": "Abreviatura (máximo 8 letras)",
	"association": "Associação",
	"team": "Equipa",
	"new": "Criar uma nova Equipa",
	"updateTeam": "Atualizar Equipa",
	"create": "Criar",
	"update": "Atualizar",
    "error": {
        "required": "Não pode estar vazio",
		"maxLen": "No máximo só pode ter {count} caratéres",
		"team": "Não foi possível receber a equipa",
		"create": "Não foi possível criar a equipa",
		"update": "Não foi possível atualizar a equipa",
		"name": "Já existe uma equipa com este nome",
		"abbreviation": "Já existe uma equipa com esta abreviatura",
    }
  },
}
</i18n>
