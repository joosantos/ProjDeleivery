<template>
	<div class="custom-input-div -mt-2">
		<div :class="['custom-input-inner-div', error != '' ? 'bg-red-100' : '']">
			<textarea
				:id="props.name"
				v-model="state"
				:name="props.name"
				:rows="props.rows"
				placeholder=""
				class="custom-input peer mt-6 pt-0">
			</textarea>
			<label
				:for="props.name"
				:class="[
					'custom-input-label peer-focus:text-sm peer-focus:text-gray-800 peer-focus:top-2 peer-focus:-translate-y-0',
					state == '' ? 'text-base text-gray-400 top-5' : 'top-2',
				]">
				{{ props.label }}
			</label>
			<div
				v-show="error != ''"
				class="absolute right-0 top-1/2 -translate-y-1/2 pr-3 pointer-events-none">
				<ExclamationCircleIcon class="h-5 w-5 text-red-700" aria-hidden="true" />
			</div>
		</div>
		<p v-show="error != ''" class="order-last mt-1 text-sm text-red-600">
			{{ error }}
		</p>
	</div>
</template>

<script setup>
import { ExclamationCircleIcon } from "@heroicons/vue/24/solid";
import { ref, watch } from "vue";

const props = defineProps({
	// Number of rows of text area
	rows: {
		type: Number,
		required: false,
		default: 3,
	},
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
	// Error of the input field
	error: {
		type: String,
		required: true,
	},
});

let state = ref(props.optionSelected);
const emit = defineEmits(["valueChanged"]);

watch(
	() => state.value,
	(after) => {
		emit("valueChanged", after);
	}
);
</script>
