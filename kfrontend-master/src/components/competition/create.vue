<template>
	<div
		class="hidden hover:bg-amber-300 bg-amber-200 bg-amber-100 hover:bg-green-300 bg-green-200 bg-green-100" />

	<Loading v-if="loading" :size="10" />
	<div v-else class="p-6 text-center text-black">
		<p class="text-3xl font-bold text-left mb-8">{{ t("title") }}</p>

		<div class="grid grid-cols-3 gap-x-8 gap-y-4">
			<div class="col-span-1 space-y-4 mt-20">
				<CustomInput
					:label="t('name')"
					type="text"
					:name="'name'"
					:option-selected="state.name"
					:error="v$.name.$errors.length == 0 ? '' : v$.name.$errors[0].$message"
					@value-changed="(option) => (state.name = option)" />
				<DateInput
					:label="t('date.inscriptions.start')"
					:name="'inscriptionsStart'"
					:option-selected="state.inscriptionsStart"
					:error="
						vInscritpions$.inscriptionsStart.$errors.length == 0
							? ''
							: vInscritpions$.inscriptionsStart.$errors[0].$message
					"
					@value-changed="(option) => changeDate(option, 'is')" />
				<DateInput
					:label="t('date.inscriptions.end')"
					:name="'inscriptionsEnd'"
					:option-selected="state.inscriptionsEnd"
					:error="
						vInscritpions$.inscriptionsEnd.$errors.length == 0
							? ''
							: vInscritpions$.inscriptionsEnd.$errors[0].$message
					"
					@value-changed="(option) => changeDate(option, 'ie')" />
				<DateInput
					:label="t('date.competition.start')"
					:name="'competitionStart'"
					:option-selected="state.competitionStart"
					:error="
						v$.competitionStart.$errors.length == 0
							? ''
							: v$.competitionStart.$errors[0].$message
					"
					@value-changed="(option) => changeDate(option, 'cs')" />
				<DateInput
					:label="t('date.competition.end')"
					:name="'competitionEnd'"
					:option-selected="state.competitionEnd"
					:error="
						v$.competitionEnd.$errors.length == 0
							? ''
							: v$.competitionEnd.$errors[0].$message
					"
					@value-changed="(option) => changeDate(option, 'ce')" />
			</div>
			<div class="relative col-start-2 row-start-1 row-span-full col-span-1">
				<Calendar
					:update="update"
					:events="[]"
					:start="startArray"
					:end="endArray"
					@update-end="update = false" />
			</div>

			<div class="col-span-1 space-y-4 mt-20 flex flex-col">
				<p class="text-lg font-medium">{{ t("legend") }}</p>
				<div class="inline-flex max-w-max mx-auto">
					<div class="w-7 h-7 bg-green-200 border border-black rounded-full" />
					<p class="ml-2">{{ t("days.inscriptions") }}</p>
				</div>
				<div class="inline-flex max-w-max mx-auto">
					<div class="w-7 h-7 bg-amber-200 border border-black rounded-full" />
					<p class="ml-2">{{ t("days.competition") }}</p>
				</div>
				<div class="inline-flex max-w-max mx-auto">
					<div class="w-7 h-7 bg-blue-200 border border-black rounded-full" />
					<p class="ml-2">{{ t("days.today") }}</p>
				</div>
			</div>
			<div class="relative mt-20 row-start-6 col-start-2">
				<Button
					:loading="showSpinningWheel"
					:show-x="showX"
					:show-check="showCheck"
					:message="props.competitionId == '' ? t('create') : t('update')"
					type="primary"
					@button-click="createCompetition" />
			</div>
		</div>
	</div>
</template>

<script setup>
import Loading from "@/components/partials/loading.vue";
import DateInput from "@/components/partials/inputs/dateInput.vue";
import Button from "@/components/partials/button.vue";
import Calendar from "@/components/partials/inputs/calendar.vue";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import { ref } from "vue";
import { authApi, errorHandling } from "@/services/api";
import router from "@/router";
import { useI18n } from "vue-i18n";
import { required, helpers, sameAs, not } from "@vuelidate/validators";
import { useVuelidate } from "@vuelidate/core";

let { t } = useI18n();

const props = defineProps({
	// Competition ID
	competitionId: {
		type: String,
		required: false,
		default: "",
	},
});

let state = ref({
	name: "",
	inscriptionsStart: "",
	inscriptionsEnd: "",
	competitionStart: "",
	competitionEnd: "",
	competition1: "",
	competition2: "",
});

const req = helpers.withMessage(t("error.required"), required);
const iStartDate = helpers.withMessage(
	t("error.iStartDate"),
	(value) => parseDate(value) < parseDate(state.value.inscriptionsEnd)
);
const iEndDate = helpers.withMessage(
	t("error.iEndDate"),
	(value) => parseDate(value) > parseDate(state.value.inscriptionsStart)
);
const iEndDatec = helpers.withMessage(
	t("error.iEndDatec"),
	(value) => parseDate(value) < parseDate(state.value.competitionStart)
);
const cStartDate = helpers.withMessage(
	t("error.cStartDate"),
	(value) => parseDate(value) < parseDate(state.value.competitionEnd)
);
const cStartDatei = helpers.withMessage(
	t("error.cStartDatei"),
	(value) => parseDate(value) > parseDate(state.value.inscriptionsEnd)
);
const cEndDate = helpers.withMessage(
	t("error.cEndDate"),
	(value) => parseDate(value) > parseDate(state.value.competitionStart)
);

let rules = {
	name: {
		required: req,
	},
	competitionStart: {
		required: req,
		biggerThanInscriptionsEnd: cStartDatei,
		smallerThanCompetitionEnd: cStartDate,
	},
	competitionEnd: {
		required: req,
		biggerThanCompetitionStart: cEndDate,
	},
};
let rulesInscriptions = {
	inscriptionsStart: {
		required: req,
		smallerThanInscriptionsEnd: iStartDate,
	},
	inscriptionsEnd: {
		required: req,
		biggerThanInscriptionsStart: iEndDate,
		smallerThanCompetitionStart: iEndDatec,
	},
};
let rulesFromCompetition = {
	competition1: {
		required: req,
		diff: helpers.withMessage(t("error.diffComp"), not(sameAs(state.value.competition2))),
	},
	competition2: {
		required: req,
		diff: helpers.withMessage(t("error.diffComp"), not(sameAs(state.value.competition1))),
	},
};
let v$ = useVuelidate(rules, state);
let vInscritpions$ = useVuelidate(rulesInscriptions, state);
let vCompetitions$ = useVuelidate(rulesFromCompetition, state);
let update = ref(false);
let startArray = ref([]);
let endArray = ref([]);
let showSpinningWheel = ref(false);
let showX = ref(false);
let showCheck = ref(false);
let competitions = ref([]);
let loading = ref(true);
let loadingCompetitions = ref(true);

if (props.competitionId != "") {
	authApi
		.get(`competitions/${props.competitionId}`)
		.then((response) => {
			startArray.value = [
				{ date: new Date(response.data.inscriptions_start), color: "green" },
				{ date: new Date(response.data.competition_start), color: "amber" },
			];
			endArray.value = [
				{ date: new Date(response.data.inscriptions_end), color: "green" },
				{ date: new Date(response.data.competition_end), color: "amber" },
			];
			let aux = new Date(response.data.inscriptions_start);
			state.value.inscriptionsStart =
				aux.getDate().toString().padStart(2, 0) +
				"-" +
				(aux.getMonth() + 1).toString().padStart(2, 0) +
				"-" +
				aux.getFullYear().toString();
			aux = new Date(response.data.inscriptions_end);
			state.value.inscriptionsEnd =
				aux.getDate().toString().padStart(2, 0) +
				"-" +
				(aux.getMonth() + 1).toString().padStart(2, 0) +
				"-" +
				aux.getFullYear().toString();
			aux = new Date(response.data.competition_start);
			state.value.competitionStart =
				aux.getDate().toString().padStart(2, 0) +
				"-" +
				(aux.getMonth() + 1).toString().padStart(2, 0) +
				"-" +
				aux.getFullYear().toString();
			aux = new Date(response.data.competition_end);
			state.value.competitionEnd =
				aux.getDate().toString().padStart(2, 0) +
				"-" +
				(aux.getMonth() + 1).toString().padStart(2, 0) +
				"-" +
				aux.getFullYear().toString();
			state.value.name = response.data.name;
			loading.value = false;
		})
		.catch((error) => {
			errorHandling(error, true);
			loading.value = false;
		});
} else {
	loading.value = false;
}

function parseDate(dateString) {
	let aux = dateString.split("-");
	return new Date(aux[2], aux[1] - 1, aux[0]);
}

function changeDate(date, pos) {
	let aux = [];
	switch (pos) {
		case "is":
			state.value.inscriptionsStart = date;
			aux = parseDate(date);
			if (startArray.value.find((a) => a.color == "green") == null) {
				startArray.value.push({ date: null, color: "green" });
			}
			startArray.value.find((a) => a.color == "green").date = aux;
			break;
		case "ie":
			state.value.inscriptionsEnd = date;
			aux = parseDate(date);
			if (endArray.value.find((a) => a.color == "green") == null) {
				endArray.value.push({ date: null, color: "green" });
			}
			endArray.value.find((a) => a.color == "green").date = aux;
			break;
		case "cs":
			state.value.competitionStart = date;
			aux = parseDate(date);
			if (startArray.value.find((a) => a.color == "amber") == null) {
				startArray.value.push({ date: null, color: "amber" });
			}
			startArray.value.find((a) => a.color == "amber").date = aux;
			break;
		case "ce":
			state.value.competitionEnd = date;
			aux = parseDate(date);
			if (endArray.value.find((a) => a.color == "amber") == null) {
				endArray.value.push({ date: null, color: "amber" });
			}
			endArray.value.find((a) => a.color == "amber").date = aux;
			break;
	}
	update.value = true;
}

async function createCompetition() {
	showX.value = false;
	showCheck.value = false;
	showSpinningWheel.value = true;

	let isFormValid = await v$.value.$validate();
	let requestData = {
		name: state.value.name,
		competition_start: state.value.competitionStart,
		competition_end: state.value.competitionEnd,
	};

	isFormValid = isFormValid && (await vInscritpions$.value.$validate());
	requestData["inscriptions_start"] = state.value.inscriptionsStart;
	requestData["inscriptions_end"] = state.value.inscriptionsEnd;

	if (!isFormValid) {
		showX.value = true;
		showSpinningWheel.value = false;
		return;
	}

	let promise =
		props.competitionId == ""
			? authApi.post("competitions", requestData)
			: authApi.put(`competitions/${props.competitionId}`, requestData);

	promise
		.then((response) => {
			showSpinningWheel.value = false;
			showCheck.value = true;
			router.push({
				name: "Competition Details",
				params: { competitionId: response.data.id },
			});
		})
		.catch((error) => {
			showSpinningWheel.value = false;
			showX.value = true;
			errorHandling(error, true);
		});
}
</script>

<i18n>
{
  	"en_GB": {
		"title": "Create a new Competition",
		"competitionFrom": {
			"first": "Create From Competition 1",
			"second": "Create From Competition 2",
		},
		"name": "Competition Name",
		"create": "Create",
		"update": "Update",
		"legend": "Legend:",
        "date": {
            "competition": {
                "start": "Starting Date of the Competition",
                "end": "Final Date of the Competition"
            },
            "inscriptions": {
                "start": "Starting Date of the Inscriptions",
                "end": "Final Date of the Inscriptions"
            },
        },
		"days": {
			"inscriptions": "-- Inscription Days",
			"competition": "-- Competition Days",
			"today": "-- Today"
		},
        "error": {
            "required": "This field is required",
			"iStartDate": "The Inscriptions Start Date must be smaller than the Inscriptions End Date",
			"iEndDate": "The Inscriptions End Date must be bigger than the Inscriptions Start Date",
			"iEndDatec": "The Inscriptions End Date must be smaller than the Competition Start Date",
			"cStartDatei": "The Competition Start Date must be bigger than the Inscriptions End Date",
			"cStartDate": "The Competition Start Date must be smaller than the Competition End Date",
			"cEndDate": "The Competition End Date must be bigger than the Competition Start Date",
			"diffDate": "The Competitions Must Be Different",
        }
	},
	"pt_PT": {
		"title": "Criar uma nova Competição",
		"competitionFrom": {
			"first": "Criar a partir da competição 1",
			"second": "Criar a partir da competição 2",
		},
		"name": "Nome da Competição",
		"create": "Criar",
		"update": "Atualizar",
		"legend": "Legenda:",
        "date": {
            "competition": {
                "start": "Data Inicial da Competição",
                "end": "Data Final da Competição"
            },
            "inscriptions": {
                "start": "Data Inicial das Inscrições",
                "end": "Data Final das Inscrições"
            },
        },
		"days": {
			"inscriptions": "-- Dias de Inscrição",
			"competition": "-- Dias de Competição",
			"today": "-- Hoje"
		},
        "error": {
            "required": "This field is required",
			"iStartDate": "A Data Inicial de Inscrições tem de ser inferior à Data Final de Inscrições",
			"iEndDate": "Data Final de Inscrições tem de superior que a Data Inicial de Inscrições",
			"iEndDatec": "A Data Final de Inscrições tem de ser inferior que à Data Inicial da Competição",
			"cStartDatei": "A Data Inicial da Competição tem de ser superior que à Data Final de Inscrições",
			"cStartDate": "A Data Inicial da Competição tem de ser inferior que à Data Final da Competição",
			"cEndDate": "A Data Final da Competição tem de ser superior que à Data Inicial da Competição",
			"diffDate": "As Competições têm de ser diferentes",
        }
	}
}
</i18n>
