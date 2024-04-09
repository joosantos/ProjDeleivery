<template>
	<div
		:class="[
			'text-center border w-10 h-10 relative select-none rounded-full',
			props.active ? 'bg-blue-300 border-blue-700' : 'bg-blue-100 border-blue-500',
			props.clickable && 'cursor-pointer hover:bg-blue-200',
		]">
		<div class="inset-0 absolute">
			<p class="relative top-1/2 -translate-y-1/2">{{ props.text }}</p>
		</div>
	</div>
</template>

<script setup>
const props = defineProps({
	text: {
		type: String,
		required: true,
	},
	active: {
		type: Boolean,
		required: true,
	},
	clickable: {
		type: Boolean,
		required: false,
		default: true,
	},
});
</script>
