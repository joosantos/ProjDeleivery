<template>
	<div :class="('w-full', props.readonly && 'opacity-50')">
		<label
			:for="props.name"
			:class="[
				'block font-medium',
				props.sizeText == 'medium' ? ' text-sm' : 'text-lg font-medium',
				props.labelBlack ? 'text-black' : 'text-gray-700',
			]"
			>{{ label }}</label
		>
		<div class="relative mt-1 rounded-md shadow-sm">
			<input
				:id="props.id == null ? props.name : props.id"
				type="file"
				:name="props.name"
				:class="[
					'block w-full rounded-md pr-10',
					props.sizeText == 'medium' ? ' sm:text-sm' : ' sm:text-lg font-semibold',
					error == ''
						? [
								'shadow-sm focus:border-indigo-500 focus:ring-indigo-500',
								props.borderBlack ? 'border-black' : 'border-gray-300',
						  ]
						: 'border-red-300 text-red-900 placeholder-red-300 focus:border-red-500 focus:outline-none focus:ring-red-500',
				]"
				:placeholder="props.placeholder"
				:aria-invalid="error != ''"
				:disabled="props.readonly || props.disabled"
				:aria-describedby="props.name + '-error'"
				:accept="props.acceptTypes"
				@change="saveFile" />
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
	// Name of the input for internal reference
	name: {
		type: String,
		required: true,
	},
	// ID of the input for internal reference
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
	// Error of the input field
	error: {
		type: String,
		required: true,
	},
	readonly: {
		type: Boolean,
		required: false,
		default: false,
	},
	disabled: {
		type: Boolean,
		required: false,
		default: false,
	},
	borderBlack: {
		type: Boolean,
		required: false,
		default: false,
	},
	labelBlack: {
		type: Boolean,
		required: false,
		default: false,
	},
	acceptTypes: {
		type: String,
		required: false,
		default: "",
	},
	sizeText: {
		type: String,
		required: false,
		default: "medium",
		validator(value) {
			// The sizeText must match one of these strings
			return ["small", "medium", "large"].includes(value);
		},
	},
});

const emit = defineEmits(["valueChanged"]);

const saveFile = (e) => {
	if (e.target.files.length == 0) emit("valueChanged", null);
	else emit("valueChanged", e.target.files[0]);
};
</script>
