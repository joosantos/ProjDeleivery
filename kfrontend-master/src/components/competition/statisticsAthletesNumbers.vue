<template>
	<Loading v-if="loading" :size="10" />
	<div v-else>
		<p class="text-3xl font-medium">{{ t("competitionName") }}</p>
		<div class="grid grid-cols-2 md:grid-cols-4 xl:grid-cols-8 mt-4 gap-y-2 gap-x-4">
			<CustomInput
				type="text"
				mask="###"
				:label="t('form.ageMin')"
				:name="'ageMin'"
				:option-selected="state.ageMin"
				:error="''"
				@value-changed="(option) => (state.ageMin = option)" />
			<CustomInput
				type="text"
				mask="###"
				:label="t('form.ageMax')"
				:name="'ageMax'"
				:option-selected="state.ageMax"
				:error="''"
				@value-changed="(option) => (state.ageMax = option)" />
			<CustomInput
				type="text"
				mask="##"
				:label="t('form.day')"
				:name="'day'"
				:option-selected="state.day"
				:error="''"
				@value-changed="(option) => (state.day = option)" />
			<SearchSelect
				:options="[
					{ id: null, name: t('all') },
					{ id: true, name: t('time.morning') },
					{ id: false, name: t('time.afternoon') },
				]"
				:title="t('form.time')"
				:option-selected="state.time"
				:error="''"
				@selected="(option) => (state.time = option)" />
			<SearchSelect
				:options="[
					{ id: null, name: t('all') },
					{ id: true, name: t('gender.male') },
					{ id: false, name: t('gender.female') },
				]"
				:title="t('form.gender')"
				:option-selected="state.gender"
				:error="''"
				@selected="(option) => (state.gender = option)" />
			<SearchSelect
				:options="[
					{ id: null, name: t('all') },
					{ id: true, name: t('adapted.yes') },
					{ id: false, name: t('adapted.no') },
				]"
				:title="t('form.adapted')"
				:option-selected="state.adapted"
				:error="''"
				@selected="(option) => (state.adapted = option)" />
			<div class="col-span-2 xl:col-span-1 mt-auto">
				<Button
					:message="t('search')"
					:type="'primary'"
					:pill="true"
					@button-click="getAthletes()" />
			</div>
		</div>
		<Loading v-if="showLoading" />
		<div v-else class="w-full flex flex-col mt-8">
			<div
				v-for="result of results"
				:key="result.id"
				class="flex w-full xl:grid xl:grid-cols-8">
				<p class="col-span-4 text-xl font-medium">{{ result.message }}</p>
				<p class="col-span-2 text-xl font-medium ml-auto xl:ml-0">{{ result.count }}</p>
			</div>
		</div>
	</div>
</template>

<script setup>
import Loading from "@/components/partials/loading.vue";
import CustomInput from "@/components/partials/inputs/customInput.vue";
import SearchSelect from "@/components/partials/inputs/searchSelect.vue";
import Button from "@/components/partials/button.vue";
import { unauthApi } from "@/services/api";
import { ref } from "vue";
import toast from "@/toast.js";
import { useI18n } from "vue-i18n";

let { t } = useI18n();

const props = defineProps({
	// ID of the competition
	competition: {
		type: String,
		required: true,
	},
});

let loading = ref(true);
let showLoading = ref(false);
let results = ref([]);
let state = ref({
	ageMin: "",
	ageMax: "",
	day: "",
	time: null,
	gender: null,
	adapted: null,
});

function getAthletes() {
	showLoading.value = true;
	let url = `competitions/${props.competition}/athletes`;
	if (
		state.value.ageMin != "" ||
		state.value.ageMax != "" ||
		state.value.day != "" ||
		state.value.time != null ||
		state.value.gender != null ||
		state.value.adapted != null
	) {
		url += "?";
		if (state.value.ageMin) {
			url += `age_min=${state.value.ageMin}&`;
		}
		if (state.value.ageMax) {
			url += `age_max=${state.value.ageMax}&`;
		}
		if (state.value.day) {
			url += `day=${state.value.day}&`;
		}
		if (state.value.time) {
			url += `time=${state.value.time}&`;
		}
		if (state.value.gender) {
			url += `gender=${state.value.gender}&`;
		}
		if (state.value.adapted) {
			url += `adapted=${state.value.adapted}&`;
		}
		url = url.slice(0, url.length - 1);
	}
	console.log(url);
	unauthApi
		.get(url)
		.then((response) => {
			console.log(response.data);
			let message = t("message.start");
			if (
				!(
					state.value.ageMin == "" &&
					state.value.ageMax == "" &&
					state.value.day == "" &&
					state.value.gender == null &&
					state.value.time == null &&
					state.value.adapted == null
				)
			) {
				message = t("message.start");
				if (state.value.ageMin == "") {
					if (state.value.ageMax != "") {
						message += t("message.ageMax", { age: state.value.ageMax });
					}
				} else {
					if (state.value.ageMax == "") {
						message += t("message.ageMin", { age: state.value.ageMin });
					} else {
						message += t("message.ages", {
							ageMin: state.value.ageMin,
							ageMax: state.value.ageMax,
						});
					}
				}
				if (state.value.day != "") {
					message += t("message.day", { day: state.value.day });
				}
				if (state.value.time != null) {
					message += t(`message.time.${state.value.time ? "morning" : "afternoon"}`);
				}
				if (state.value.gender != null) {
					message += t(`message.gender.${state.value.time ? "male" : "female"}`);
				}
				if (state.value.adapted != null) {
					message += t(`message.adapted.${state.value.time ? "yes" : "no"}`);
				}
				message = message.slice(0, message.length - 2);
			}
			results.value.push({
				id: results.value.length,
				message: message,
				count: response.data,
			});
			loading.value = false;
			showLoading.value = false;
		})
		.catch((e) => {
			console.log(e);
			toast.error(t("tournament.notLoaded"));
		});
}
getAthletes();
</script>

<i18n>
{
  "en_GB": {
	"competitionName": "Competition {name} Athletes Statistics",
	"all": "All",
	"search": "Get Athletes",
	"form": {
		"ageMin": "Minimum Age",
		"ageMax": "Maximum Age",
		"day": "Competition Day",
		"time": "Time of the day",
		"gender": "Gender",
		"adapted": "Adapted",
		"filter": "Filter Results"
	},
	"time": {
		"morning": "Morining",
		"afternoon": "Afternoon",
	},
	"gender": {
		"male": "Male",
		"female": "Female",
	},
	"adapted": {
		"yes": "Adapted",
		"no": "Not Adapted",
	},
	"message": {
		"start": "Number of athletes ",
		"ageMin": "+{age} years, ",
		"ageMax": "-{age} years, ",
		"ages": "{ageMin}-{ageMax} years, ",
		"day": "day {day}, ",
		"time": {
			"morning": "morning, ",
			"afternoon": "afternoon, ",
		},
		"gender": {
			"male": "male, ",
			"female": "female, "
		},
		"adapted": {
			"yes": "adapted, ",
			"no": "not adapted, "
		},
	}
  },
  "pt_PT": {
	"competitionName": "Estatísticas de Atletas da Competição {name}",
	"all": "Todos",
	"search": "Obter Atletas",
	"form": {
		"ageMin": "Idade Mínima",
		"ageMax": "Idade Máxima",
		"day": "Dia da Competição",
		"time": "Altura do dia",
		"gender": "Género",
		"adapted": "Adaptado",
		"filter": "Filtrar Resultados"
	},
	"time": {
		"morning": "Manhã",
		"afternoon": "Tarde",
	},
	"gender": {
		"male": "Masculino",
		"female": "Feminino",
	},
	"adapted": {
		"yes": "Adaptado",
		"no": "Não Adaptado",
	},
	"message": {
		"startOnly": "Número de Atletas ",
		"ageMin": "+{age} anos, ",
		"ageMax": "-{age} anos, ",
		"ages": "{ageMin}-{ageMax} anos, ",
		"day": "dia {day}, ",
		"time": {
			"morning": "manhã, ",
			"afternoon": "tarde, ",
		},
		"gender": {
			"male": "masculino, ",
			"female": "feminino, "
		},
		"adapted": {
			"yes": "adaptado, ",
			"no": "não adaptado, "
		},
	}
  }
}
</i18n>
