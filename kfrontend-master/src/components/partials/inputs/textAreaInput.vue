<template>
	<div :class="['w-full border-none bg-transparent', props.readonly && 'opacity-50']">
		<label for="comment" class="block text-sm font-medium text-gray-700 text-left">
			{{ props.label }}
		</label>
		<div class="mt-1 relative">
			<textarea
				:id="props.id == null ? props.name : props.id"
				v-model="state"
				:rows="props.rows"
				:name="props.name"
				:disabled="props.readonly"
				:class="[
					'block w-full rounded-md shadow-sm sm:text-sm',
					error == ''
						? 'border-gray-300 focus:border-indigo-500 focus:ring-indigo-500'
						: 'border-red-300 text-red-900 placeholder-red-300 focus:border-red-500 focus:outline-none focus:ring-red-500',
				]" />
			<div
				v-if="error != ''"
				class="pointer-events-none absolute inset-y-0 right-0 flex items-center pr-3">
				<ExclamationCircleIcon class="h-5 w-5 text-red-500" aria-hidden="true" />
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
	// Name of the input for internal reference
	id: {
		type: String,
		required: false,
		default: null,
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
	// Read Only Option
	readonly: {
		type: Boolean,
		required: false,
		default: false,
	},
});

let state = ref(props.optionSelected);
const emit = defineEmits(["valueChanged"]);

watch(
	() => props.optionSelected,
	(after) => {
		state.value = after;
	}
);

watch(
	() => state.value,
	(after) => {
		emit("valueChanged", after);
	}
);
</script>
