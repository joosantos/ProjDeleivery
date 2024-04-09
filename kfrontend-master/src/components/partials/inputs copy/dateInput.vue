<template>
	<div class="custom-input-div">
		<div
			:class="[
				'custom-input-inner-div pb-7',
				error != '' ? 'bg-red-100' : '',
				props.readonly && 'opacity-25 pointer-events-none select-none',
			]">
			<input
				:id="props.name + 'Input'"
				v-model="auxDate"
				:name="props.name"
				type="date"
				class="transition-all duration-200 peer opacity-0 z-10 h-full w-full absolute left-0 top-0" />

			<label
				:for="props.name"
				:class="[
					'custom-input-label peer-focus:text-sm peer-focus:text-gray-800 peer-focus:top-2 peer-focus:-translate-y-0',
					state == ''
						? 'text-base text-gray-400 top-1/2 -translate-y-1/2'
						: 'text-black top-2',
				]">
				{{ props.label }}
			</label>

			<div
				:id="props.name"
				:name="props.name"
				:class="[
					'block relative bg-transparent top-5 text-left',
					error != '' ? 'bg-red-100' : '',
					state == '' ? 'pb-8' : 'text-black',
				]">
				{{ state == "" ? "" : state }}
			</div>

			<CalendarIcon
				:class="[
					'h-5 absolute mr-3 pointer-events-none top-1/2 -translate-y-1/2',
					error != '' ? 'right-6' : 'right-0',
				]" />
			<div
				v-show="error != ''"
				class="absolute right-0 top-1/2 -translate-y-1/2 mr-3 pointer-events-none">
				<ExclamationCircleIcon class="h-5 w-5 text-red-700" aria-hidden="true" />
			</div>
		</div>
		<p v-show="error != ''" class="relative text-sm mt-1 text-red-600">
			{{ error }}
		</p>
	</div>
</template>

<script setup>
import { ExclamationCircleIcon } from "@heroicons/vue/24/solid";
import { CalendarIcon } from "@heroicons/vue/24/outline";
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
	// Value of the selected option if any
	optionSelected: {
		type: String,
		required: false,
		default: "",
	},
	readonly: {
		type: Boolean,
		required: false,
		default: false,
	},
	// Error of the input field
	error: {
		type: String,
		required: true,
	},
});

let state = ref(props.optionSelected);
let aux = new Date();
if (state.value != "") {
	let auxD = state.value.split("-");
	aux = new Date(auxD[2], auxD[1], auxD[0]);
}
let auxDate = ref(aux.getFullYear() + "-" + aux.getMonth() + "-" + aux.getDate());
const emit = defineEmits(["valueChanged"]);
let control = false;

watch(
	() => state.value,
	(after, before) => {
		if (control) {
			control = false;
			return;
		}
		if (props.readonly) {
			state.value = before;
			control = true;
			return;
		}
		emit("valueChanged", after);
	}
);

watch(
	() => auxDate.value,
	() => {
		let aux = document.getElementById(props.name + "Input")?.valueAsDate;
		if (aux == null) {
			return;
		}
		state.value =
			aux.getDate().toString().padStart(2, "0") +
			"-" +
			(aux.getMonth() + 1).toString().padStart(2, "0") +
			"-" +
			aux.getFullYear();
	}
);
</script>
