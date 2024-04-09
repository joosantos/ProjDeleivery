<template>
	<div
		:class="[
			'absolute left-1/2 -translate-x-1/2 border-2 border-black bg-gray-200  rounded-full px-2',
			props.bigTimer ? 'w-[1000px] py-0 bottom-10 h-60' : 'w-[700px] py-2 bottom-28 h-40',
		]">
		<p
			:class="[
				'text-center font-semibold relative top-1/2 -translate-y-1/2 uppercase',
				props.bigTimer ? 'text-[225px]' : 'text-[160px]',
			]">
			{{ time }}
		</p>
	</div>
</template>
<script setup>
import { ref } from "vue";
const props = defineProps({
	bigTimer: {
		type: Boolean,
		required: true,
	},
});

let time = ref("00:00");

setInterval(() => {
	time.value = localStorage.getItem("matchTimer") || "00:00";
}, 100);
</script>
