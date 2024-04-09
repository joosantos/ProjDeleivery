<template>
	<div :class="('w-full', props.readonly && 'opacity-50')">
		<label :for="props.name" class="block text-sm font-medium text-gray-700">{{ label }}</label>
		<div class="relative mt-1">
			<input
				:id="props.id == null ? props.name + '-date-input' : props.id + '-date-input'"
				v-model="dateInput"
				:disabled="props.readonly"
				type="date"
				:name="props.name + '-date-input'"
				class="opacity-0 z-10 h-full w-full absolute left-0 top-0" />

			<div
				:id="props.name"
				:name="props.name"
				:class="[
					'w-full rounded-md border  bg-white py-2 pl-3 pr-10 shadow-sm focus:outline-none focus:ring-1 sm:text-sm',
					error == ''
						? 'border-gray-300 focus:border-indigo-500 focus:ring-indigo-500'
						: 'border-red-300 text-red-900 focus:border-red-500 focus:ring-red-500',
				]">
				{{ state == "" ? "&nbsp;" : state }}
			</div>

			<CalendarIcon
				:class="[
					'h-5 absolute mr-3 pointer-events-none top-1/2 -translate-y-1/2',
					error != '' ? 'right-6' : 'right-0',
				]" />
			<div
				v-if="error != ''"
				class="absolute right-0 top-1/2 -translate-y-1/2 mr-3 pointer-events-none">
				<ExclamationCircleIcon class="h-5 w-5 text-red-700" aria-hidden="true" />
			</div>
		</div>
		<p
			v-if="error != ''"
			:id="props.id == null ? props.name : props.id"
			class="mt-2 text-sm text-red-600">
			{{ error }}
		</p>
	</div>
</template>

<script setup>
import { ExclamationCircleIcon } from "@heroicons/vue/24/solid";
import { CalendarIcon } from "@heroicons/vue/24/outline";
import { ref, watch, computed } from "vue";

const props = defineProps({
	// Name of the input for internal reference
	name: {
		type: String,
		required: true,
	},
	// Label of the input to be displayed
	label: {
		type: String,
		required: true,
	},
	// Value of the selected option if any format: "day-month-year", example: "05-10-2022"
	optionSelected: {
		type: String,
		required: false,
		default: "",
	},
	// Error of the input field
	error: {
		type: String,
		required: true,
	},
	// Read Only Option
	readonly: {
		type: Boolean,
		required: false,
		default: false,
	},
});

const emit = defineEmits(["valueChanged"]);
let dateInput = ref("");
let state = computed(() => {
	if (dateInput.value == "") {
		return "";
	}
	let aux = new Date(dateInput.value);
	if (aux == null) {
		return;
	}
	return `${aux.getDate().toString().padStart(2, "0")}-${(aux.getMonth() + 1)
		.toString()
		.padStart(2, "0")}-${aux.getFullYear()}`;
});

let auxDate = computed(() => {
	let splited = props.optionSelected.split("-");
	if (splited.length != 3) {
		return "";
	}
	return `${splited[2]}-${Number(splited[1])}-${splited[0]}`;
});
watch(
	() => auxDate.value,
	(after) => {
		dateInput.value = after;
	},
	{ immediate: true }
);

watch(
	() => state.value,
	(after) => {
		emit("valueChanged", after);
	}
);
</script>
