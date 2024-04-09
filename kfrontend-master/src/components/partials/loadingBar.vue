<template>
	<div>
		<div
			:class="[
				'w-full rounded-full bg-gray-200 border border-gray-500',
				props.size === 'medium' ? 'h-5' : 'h-3',
			]">
			<div
				:style="`width: ${props.progress}%`"
				:class="[
					'h-full rounded-full ',
					props.variant === 'success'
						? 'bg-gradient-to-r from-green-500 via-lime-300 to-green-500'
						: props.variant === 'warning'
						? 'bg-gradient-to-r from-yellow-300 via-amber-100 to-yellow-300'
						: props.variant === 'danger'
						? 'bg-gradient-to-r from-red-600 via-rose-300 to-red-600'
						: 'bg-gradient-to-r from-blue-500 via-sky-300 to-blue-500',
				]" />
		</div>
	</div>
</template>

<script setup>
const props = defineProps({
	progress: {
		type: Number,
		required: true,
		validator: function (value) {
			return value >= 0 && value <= 100;
		},
	},
	variant: {
		type: String,
		required: false,
		default: "primary",
		validator: function (value) {
			// The value must match one of these strings
			return ["primary", "success", "warning", "danger"].includes(value);
		},
	},
	size: {
		type: String,
		required: false,
		default: "medium",
		validator: function (value) {
			// The value must match one of these strings
			return ["medium", "small"].includes(value);
		},
	},
});
</script>
