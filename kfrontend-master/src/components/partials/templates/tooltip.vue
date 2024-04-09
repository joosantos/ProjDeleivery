<template>
	<div :class="show ? 'relative group' : 'p-0 m-0'">
		<slot></slot>
		<span
			v-if="show"
			:class="[
				'max-w-lg w-max invisible opacity-0 duration-300 bg-black text-white text-center py-1 px-2 bottom-full absolute z-10 left-1/2 -translate-x-1/2 group-hover:visible group-hover:opacity-100 rounded-md text-base font-normal',
				props.capitalize && 'capitalize',
			]">
			{{ props.text }}
		</span>
	</div>
</template>

<script setup>
const props = defineProps({
	show: {
		type: Boolean,
		required: false,
		default: true,
	},
	text: {
		type: String,
		required: true,
	},
	capitalize: {
		type: Boolean,
		required: false,
		default: false,
	},
});
</script>
