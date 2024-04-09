<template>
	<div :class="('w-full', props.readonly && 'opacity-50')">
		<label :for="props.name" class="block text-sm font-medium text-gray-700">{{ label }}</label>
		<div class="relative mt-1">
			<input
				:id="props.id == null ? props.name + '-date-input' : props.id + '-date-input'"
				v-model="date"
				:disabled="props.readonly"
				type="date"
				:name="props.name + '-date-input'"
				:class="[
					'w-full rounded-md border bg-white py-2 pl-3 shadow-sm focus:outline-none focus:ring-1 sm:text-sm',
					error == ''
						? 'border-gray-300 focus:border-indigo-500 focus:ring-indigo-500'
						: 'border-red-300 text-red-900 focus:border-red-500 focus:ring-red-500 pr-8',
				]"
				@input="emitEvent()" />

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
import { ref, watch } from "vue";

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
let date = ref(getDateFromProps(props.optionSelected));

watch(
	() => props.optionSelected,
	(after) => {
		date.value = getDateFromProps(after);
	}
);

function getDateFromProps(dateIn) {
	if (dateIn == null) return null;
	let splited = dateIn.split("-");
	if (splited[0] > 50) return dateIn;
	return `${splited[2]}-${splited[1]}-${splited[0]}`;
}

function emitEvent() {
	let splited = date.value.split("-");
	let emitDate = `${splited[2]}-${splited[1]}-${splited[0]}`;
	emit("valueChanged", emitDate);
}
</script>
