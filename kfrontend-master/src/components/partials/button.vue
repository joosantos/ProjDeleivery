<template>
	<button
		:tabindex="props.disabled && '-1'"
		:class="[
			'border-2 z-0 w-full shadow-sm focus:outline-none select-none cursor-pointer focus:ring-2 focus:ring-offset-2 relative',
			props.size == 'normal'
				? 'py-2 px-4 text-base font-medium'
				: props.size == 'small'
				? props.showX || props.showCheck
					? 'py-0 pr-10 text-base font-normal'
					: 'py-0 px-2 text-base font-normal'
				: 'py-4 px-8 text-lg font-semibold',
			props.upOnHover ? 'hover:-translate-y-0.5' : '',
			props.showSpinningWheel || props.showCheck ? 'pointer-events-none opacity-50' : '',
			props.pill ? 'rounded-3xl' : 'rounded-md',
			props.outline ? 'font-medium' : 'border-transparent hover:shadow-lg',
			props.disabled && 'pointer-events-none cursor-not-allowed opacity-50 none',
			props.type == 'primary'
				? props.outline
					? 'border-blue-600 text-blue-700 hover:bg-blue-300 hover:text-blue-800 focus:ring-blue-600 active:bg-blue-400'
					: 'text-white border-blue-500 hover:border-blue-700 active:border-blue-900 bg-blue-500 hover:bg-blue-600 active:bg-blue-700 focus:ring-blue-700'
				: props.type == 'secondary'
				? props.outline
					? 'border-primary-400 text-primary-400 hover:bg-primary-400 hover:text-white focus:ring-primary-400 active:bg-primary-300'
					: 'text-white border-primary-400 hover:border-primary-300 active:border-primary-500 bg-primary-400 hover:bg-primary-300 active:bg-primary-500 focus:ring-primary-600'
				: props.type == 'success'
				? props.outline
					? 'border-green-600 text-green-600 hover:bg-green-600 hover:text-white focus:ring-green-600 active:bg-green-500'
					: 'text-white border-green-600 hover:border-green-500 active:border-green-700 bg-green-600 hover:bg-green-500 active:bg-green-700 focus:ring-green-800'
				: props.type == 'danger'
				? props.outline
					? 'border-red-600 text-red-600 hover:bg-red-600 hover:text-white focus:ring-red-600 active:bg-red-400'
					: 'text-white border-red-600 hover:border-red-500 active:border-red-700 bg-red-600 hover:bg-red-500 active:bg-red-700 focus:ring-red-800'
				: props.type == 'warning'
				? props.outline
					? 'border-yellow-400 text-yellow-500 hover:bg-yellow-400 hover:text-white focus:ring-yellow-400 active:bg-yellow-300'
					: 'text-white border-yellow-400 hover:border-yellow-300 active:border-yellow-500 bg-yellow-400 hover:bg-yellow-300 active:bg-yellow-500 focus:ring-yellow-800'
				: props.type == 'black'
				? props.outline
					? 'border-gray-800 text-gray-800 hover:bg-gray-200 hover:text-black focus:ring-black active:bg-gray-400'
					: 'text-white border-gray-800 hover:border-gray-900 active:border-black bg-gray-800 hover:bg-gray-600 active:bg-black focus:ring-gray-900'
				: props.outline
				? 'border-blue-500 text-blue-500 hover:bg-blue-500 hover:text-white focus:ring-blue-500 active:bg-blue-400'
				: 'text-white border-blue-500 hover:border-blue-400 active:border-blue-600 bg-blue-500 hover:bg-blue-400 active:bg-blue-600 focus:ring-blue-700',
		]"
		:type="props.submit ? 'submit' : 'button'"
		@click="!props.disabled && emit('buttonClick')">
		<svg v-if="props.loading" class="animate-spin w-6 h-6 mx-auto" viewBox="0 0 50 50">
			<path
				fill="currentColor"
				d="M25.251,6.461c-10.318,0-18.683,8.365-18.683,18.683h4.068c0-8.071,6.543-14.615,14.615-14.615V6.461z"></path>
		</svg>
		<div v-else>
			<div class="inline-flex justify-between w-full relative">
				<component
					:is="props.icon"
					v-if="props.icon != null"
					:class="[
						'h-5 w-5 absolute top-1/2 -translate-y-1/2',
						!props.iconLeft && 'right-0',
					]" />
				<p
					:class="[
						props.capitalize && 'capitalize',
						props.icon ? (props.iconLeft ? 'ml-8' : 'mr-8') : 'mx-auto',
					]">
					{{ props.message }}
				</p>
			</div>
		</div>
		<CheckCircleIcon
			v-show="props.showCheck"
			style="width: 24px"
			class="absolute right-0 mr-3 top-1/2 -translate-y-1/2" />
		<XCircleIcon
			v-show="props.showX"
			style="width: 24px"
			class="absolute right-0 mr-3 top-1/2 -translate-y-1/2" />
	</button>
</template>

<script setup>
import { CheckCircleIcon, XCircleIcon } from "@heroicons/vue/24/outline";

const props = defineProps({
	message: {
		type: String,
		required: true,
	},
	type: {
		required: true,
		type: String,
		validator(value) {
			// The value must match one of these strings
			return [
				"primary",
				"secondary",
				"success",
				"danger",
				"warning",
				"black",
				"info",
			].includes(value);
		},
	},
	disabled: {
		required: false,
		default: false,
		type: Boolean,
	},
	submit: {
		required: false,
		default: false,
		type: Boolean,
	},
	loading: {
		required: false,
		default: false,
		type: Boolean,
	},
	showCheck: {
		required: false,
		default: false,
		type: Boolean,
	},
	showX: {
		required: false,
		default: false,
		type: Boolean,
	},
	icon: {
		required: false,
		default: null,
		type: [Function, Object],
	},
	pill: {
		required: false,
		default: false,
		type: Boolean,
	},
	outline: {
		required: false,
		default: false,
		type: Boolean,
	},
	upOnHover: {
		required: false,
		default: true,
		type: Boolean,
	},
	iconLeft: {
		required: false,
		default: false,
		type: Boolean,
	},
	size: {
		required: false,
		default: "normal",
		type: String,
		validator: function (value) {
			// The value must match one of these strings
			return ["small", "normal", "big"].includes(value);
		},
	},
	capitalize: {
		type: Boolean,
		required: false,
		default: false,
	},
});

const emit = defineEmits(["buttonClick"]);
</script>
