<template>
	<div
		class="absolute inset-0 bg-[#F7F7F7] z-40 grid grid-cols-3 h-full bg-gradient-to-r from-[#f7f6f6] to-[#ffc68d]">
		<div id="podium2" class="opacity-0 col-span-1 col-start-1 relative mt-60 duration-1000">
			<LaurelCrown class="h-[30rem] w-[30rem] text-[#BFBFBF] mx-auto" />
			<p class="text-9xl font-bold text-[#BFBFBF] absolute top-40 text-center w-full">2º</p>
			<p class="text-9xl w-full text-center">{{ props.secondName }}</p>
		</div>
		<div id="podium1" class="opacity-0 col-span-1 col-start-2 relative mt-20 duration-1000">
			<LaurelCrown class="h-[30rem] w-[30rem] text-[#F0C419] mx-auto" />
			<p class="text-9xl font-bold text-[#f0c419] absolute top-40 text-center w-full">1º</p>
			<p class="text-9xl w-full text-center">{{ props.firstName }}</p>
		</div>
		<div id="podium3" class="opacity-0 col-span-1 col-start-3 relative mt-80 duration-1000">
			<LaurelCrown class="h-[30rem] w-[30rem] text-[#CD7F32] mx-auto" />
			<p class="text-9xl font-bold text-[#CD7F32] absolute top-40 text-center w-full">3º</p>
			<p class="text-9xl w-full text-center">{{ props.thirdName }}</p>
		</div>
	</div>
</template>
<script setup>
import LaurelCrown from "@/components/icons/laurelCrown.vue";
const props = defineProps({
	firstName: {
		type: String,
		required: false,
		default: "",
	},
	secondName: {
		type: String,
		required: false,
		default: "",
	},
	thirdName: {
		type: String,
		required: false,
		default: "",
	},
});

if (props.thirdName)
	setTimeout(() => {
		document.getElementById("podium3").classList.remove("opacity-0");
		document.getElementById("podium3").classList.remove("mt-80");
		document.getElementById("podium3").classList.add("mt-60");
	}, 500);
if (props.secondName)
	setTimeout(() => {
		document.getElementById("podium2").classList.remove("opacity-0");
		document.getElementById("podium2").classList.remove("mt-60");
		document.getElementById("podium2").classList.add("mt-40");
	}, 2000);
if (props.thirdName)
	setTimeout(() => {
		document.getElementById("podium1").classList.remove("opacity-0");
		document.getElementById("podium1").classList.remove("mt-20");
		document.getElementById("podium1").classList.add("mt-0");
	}, 3500);
</script>
