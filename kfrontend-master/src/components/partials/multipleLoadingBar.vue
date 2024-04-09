<template>
	<div>
		<div
			:class="[
				'w-full inline-flex rounded-full bg-gray-200 border border-gray-500',
				props.size === 'medium' ? 'h-5' : 'h-3',
			]">
			<div
				v-for="(bar, idx) of props.bars"
				:key="bar"
				:style="`width: ${bar.progress}%`"
				:class="[
					'h-full',
					idx === 0 ? 'rounded-l-full' : '',
					idx === props.bars.length - 1 ? 'rounded-r-full' : '',
					bar.variant === 'success'
						? 'bg-gradient-to-r from-green-500 via-lime-300 to-green-500'
						: bar.variant === 'warning'
						? 'bg-gradient-to-r from-yellow-300 via-amber-100 to-yellow-300'
						: bar.variant === 'danger'
						? 'bg-gradient-to-r from-red-600 via-rose-300 to-red-600'
						: 'bg-gradient-to-r from-blue-500 via-sky-300 to-blue-500',
				]" />
		</div>
	</div>
</template>

<script setup>
const props = defineProps({
	bars: {
		type: Object,
		required: true,
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
