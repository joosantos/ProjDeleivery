<template>
	<div
		:class="[
			'relative',
			props.secondary && 'scale-[80%] p-4 bg-blue-100 border-2 border-black rounded-lg',
		]">
		<div v-if="props.secondary" class="absolute right-2 top-2">
			<XCircleIcon
				class="h-10 w-10 text-black cursor-pointer rounded-full"
				@click="emit('hide')" />
		</div>
		<!-- Timer Title -->
		<div
			v-if="props.title !== ''"
			class="border-2 border-black border-b-0 rounded-t-lg bg-gray-400 w-max mx-auto">
			<p class="text-xl mx-auto font-medium px-4 py-1 capitalize">
				{{ props.title }}
			</p>
		</div>

		<!-- Timer Header -->
		<div
			v-if="!timerInUse && !props.secondary"
			class="text-center border-2 min-w-max max-w-min mx-auto border-black bg-gray-400 border-b-0 rounded-t-lg">
			<p>
				{{ t("tableTimer.header") }}
			</p>
			<div class="inline-flex px-1 mt-2 gap-x-2 mb-1">
				<Tooltip :text="t('tooltips.keys.z')" :capitalize="true">
					<p
						class="border border-black px-1 bg-gray-200 rounded-lg cursor-pointer select-none"
						@click="add(30)">
						+ 00:30
					</p>
				</Tooltip>
				<Tooltip :text="t('tooltips.keys.x')" :capitalize="true">
					<p
						class="border border-black px-1 bg-gray-200 rounded-lg cursor-pointer select-none"
						@click="add(60)">
						+ 01:00
					</p>
				</Tooltip>
				<Tooltip :text="t('tooltips.keys.c')" :capitalize="true">
					<p
						class="border border-black px-1 bg-gray-200 rounded-lg cursor-pointer select-none"
						@click="remove(30)">
						-- 00:30
					</p>
				</Tooltip>
				<Tooltip :text="t('tooltips.keys.v')" :capitalize="true">
					<p
						class="border border-black px-1 bg-gray-200 rounded-lg cursor-pointer select-none"
						@click="remove(60)">
						-- 01:00
					</p>
				</Tooltip>
				<Tooltip :text="t('tooltips.keys.b')" :capitalize="true">
					<p
						class="border border-black px-1 bg-red-500 rounded-lg cursor-pointer select-none"
						@click="resetTimer">
						{{ t("tableTimer.reset") }}
					</p>
				</Tooltip>
			</div>
		</div>

		<!-- Timer -->
		<div class="mx-auto border-2 border-black rounded-b-none bg-white w-[450px] rounded-lg">
			<input
				v-if="!timerInUse"
				v-model="actualTimer"
				v-mask="'##:##'"
				class="text-5xl text-center font-semibold w-full rounded-lg h-[4.25rem]"
				@input="
					initialTimer = actualTimer;
					updateTimer(false);
				" />
			<div
				v-else
				class="uppercase text-5xl text-center font-semibold w-full rounded-lg h-[4.25rem] relative">
				<p class="relative top-1/2 -translate-y-1/2">{{ actualTimer }}</p>
			</div>
		</div>

		<!-- Start and Restart Button -->
		<div class="inline-flex relative left-1/2 -translate-x-1/2">
			<!-- Restart Button padding -->
			<div
				v-if="!timerInUse && initialTimer !== actualTimer"
				class="invisible mr-2 pointer-events-none w-min bg-white border-2 border-black rounded-lg">
				<div class="relative top-1/2 -translate-y-1/2 text-xl px-2">
					<Tooltip
						v-if="!props.secondary"
						:text="t('tooltips.keys.r')"
						:capitalize="true">
						<button @click="restartTimer">
							{{ t("tableTimer.restartTimer") }}
						</button>
					</Tooltip>
					<button v-else @click="restartTimer">
						{{ t("tableTimer.restartTimer") }}
					</button>
				</div>
			</div>

			<!-- Start Button -->
			<div
				class="py-1 border-2 border-t-0 border-black rounded-t-none bg-white w-[450px] hover:bg-gray-300 rounded-lg">
				<Tooltip :text="t('tooltips.keys.space')" :capitalize="true">
					<button
						v-if="!timerInUse"
						class="text-4xl text-center font-semibold cursor-pointer w-full rounded-lg uppercase"
						@click="start">
						{{ t("start") }}
					</button>
					<button
						v-else
						class="text-4xl text-center font-semibold cursor-pointer w-full rounded-lg uppercase"
						@click="pause">
						{{ t("pause") }}
					</button>
				</Tooltip>
			</div>

			<!-- Restart Button -->
			<div
				v-if="!timerInUse && initialTimer !== actualTimer"
				class="w-min ml-2 bg-white border-2 border-black rounded-lg">
				<div class="relative top-1/2 -translate-y-1/2 text-xl px-2">
					<Tooltip
						v-if="!props.secondary"
						:text="t('tooltips.keys.r')"
						:capitalize="true">
						<button @click="restartTimer">
							{{ t("tableTimer.restartTimer") }}
						</button>
					</Tooltip>
					<button v-else @click="restartTimer">
						{{ t("tableTimer.restartTimer") }}
					</button>
				</div>
			</div>
		</div>
	</div>
</template>
<script setup>
import Tooltip from "@/components/partials/templates/tooltip.vue";
import { ref, computed } from "vue";
import { XCircleIcon } from "@heroicons/vue/24/outline";
import { useI18n } from "vue-i18n";

const props = defineProps({
	modalOpen: {
		type: Boolean,
		required: true,
	},
	secondary: {
		type: Boolean,
		required: false,
		default: false,
	},
	title: {
		type: String,
		required: false,
		default: "",
	},
	saveLocal: {
		type: Boolean,
		required: false,
		default: true,
	},
});
const emit = defineEmits(["hide"]);
let { t } = useI18n({ useScope: "global" });

let initialTimer = ref("00:00");
let actualTimer = ref("00:00");
let timerStarted = ref(false);
let timerHasEnded = ref(false);
let timerWasPaused = ref(false);
let timePromise = ref(null);
let timerInUse = computed(() => {
	return timerStarted.value || timerHasEnded.value;
});
let controlPressed = ref(false);

function start() {
	timerStarted.value = true;
	updateTimer(false);
	let countDownDate = new Date();
	countDownDate.setMinutes(countDownDate.getMinutes() + Number(actualTimer.value.split(":")[0]));
	countDownDate.setSeconds(countDownDate.getSeconds() + Number(actualTimer.value.split(":")[1]));
	countDownDate = countDownDate.getTime();

	timePromise.value = setInterval(function () {
		let now = new Date().getTime();
		let distance = countDownDate - now;

		let minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
		let seconds = Math.ceil((distance % (1000 * 60)) / 1000);
		while (seconds >= 60) {
			minutes += 1;
			seconds -= 60;
			if (seconds < 0) seconds = 0;
		}

		actualTimer.value =
			minutes.toString().padStart(2, "0") + ":" + seconds.toString().padStart(2, "0");
		updateTimer(false);
		if (distance < 0) {
			clearInterval(timePromise.value);
			timerStarted.value = false;
			timerHasEnded.value = true;
			actualTimer.value = t("end");
			updateTimer(true);
			setTimeout(removeEnd, 3000);
		}
	}, 1001);
}

function removeEnd() {
	actualTimer.value = initialTimer.value;
	timerHasEnded.value = false;
	updateTimer(false);
}

function pause() {
	clearInterval(timePromise.value);
	timerStarted.value = false;
	timerWasPaused.value = true;
	updateTimer(false);
}

function updateTimer(ended) {
	if (props.saveLocal && !props.secondary)
		localStorage.setItem("matchTimer", ended ? "END" : actualTimer.value);
}

function resetTimer() {
	if (!timerInUse.value) {
		initialTimer.value = "00:00";
		actualTimer.value = initialTimer.value;
		updateTimer(false);
	}
}

function restartTimer() {
	if (!timerInUse.value && initialTimer.value !== actualTimer.value) {
		actualTimer.value = initialTimer.value;
		updateTimer(false);
	}
}

function add(secondsToAdd) {
	if (timerInUse.value) {
		return;
	}
	if (timerWasPaused.value) {
		let aux = actualTimer.value.split(":");
		if (aux.length !== 2) aux = ["00", "00"];
		let minutes = Number(aux[0]) + Math.floor(secondsToAdd / 60);
		let seconds = Number(aux[1]) + (secondsToAdd % 60);
		if (seconds >= 60) {
			seconds = seconds - 60;
			minutes = minutes + 1;
		}
		actualTimer.value = `${minutes.toString().padStart(2, "0")}:${seconds
			.toString()
			.padStart(2, "0")}`;
	} else {
		let aux = initialTimer.value.split(":");
		let minutes = Number(aux[0]) + Math.floor(secondsToAdd / 60);
		let seconds = Number(aux[1]) + (secondsToAdd % 60);
		if (seconds >= 60) {
			seconds = seconds - 60;
			minutes = minutes + 1;
		}
		initialTimer.value = `${minutes.toString().padStart(2, "0")}:${seconds
			.toString()
			.padStart(2, "0")}`;
		actualTimer.value = initialTimer.value;
	}
	updateTimer(false);
}

function remove(secondsToRemove) {
	if (timerInUse.value) {
		return;
	}
	if (timerWasPaused.value) {
		let aux = actualTimer.value.split(":");
		if (aux.length !== 2) aux = ["00", "00"];
		let minutes = Number(aux[0]) - Math.floor(secondsToRemove / 60);
		let seconds = Number(aux[1]) - (secondsToRemove % 60);
		if (seconds < 0) {
			seconds = seconds + 60;
			minutes = minutes - 1;
		}
		if (minutes < 0) {
			minutes = 0;
			seconds = 0;
		}
		actualTimer.value = `${minutes.toString().padStart(2, "0")}:${seconds
			.toString()
			.padStart(2, "0")}`;
	} else {
		let aux = initialTimer.value.split(":");
		let minutes = Number(aux[0]) - Math.floor(secondsToRemove / 60);
		let seconds = Number(aux[1]) - (secondsToRemove % 60);
		if (seconds < 0) {
			seconds = seconds + 60;
			minutes = minutes - 1;
		}
		if (minutes < 0) {
			minutes = 0;
			seconds = 0;
		}
		initialTimer.value = `${minutes.toString().padStart(2, "0")}:${seconds
			.toString()
			.padStart(2, "0")}`;
		actualTimer.value = initialTimer.value;
	}
	updateTimer(false);
}

window.addEventListener("keyup", function (event) {
	if (event.code.indexOf("Control") != -1) {
		controlPressed.value = false;
		return;
	}
});

window.addEventListener("keydown", function (event) {
	if (
		props.secondary ||
		event.target.tagName == "INPUT" ||
		event.target.tagName == "TEXTAREA" ||
		props.modalOpen ||
		controlPressed.value
	) {
		return;
	}

	if (event.code.indexOf("Control") != -1) {
		controlPressed.value = true;
		return;
	}
	switch (event.code) {
		case "KeyZ":
			event.preventDefault();
			add(30);
			break;
		case "KeyX":
			event.preventDefault();
			add(60);
			break;
		case "KeyC":
			event.preventDefault();
			remove(30);
			break;
		case "KeyV":
			event.preventDefault();
			remove(60);
			break;
		case "KeyB":
			event.preventDefault();
			resetTimer();
			break;
		case "KeyR":
			event.preventDefault();
			restartTimer();
			break;
		case "Space":
			event.preventDefault();
			if (timerInUse.value) {
				pause();
			} else {
				start();
			}
			break;
	}
});
</script>
