<template>
	<div
		v-for="(cal, s) of calendars"
		:key="cal"
		:class="['grid grid-cols-12 gap-x-8', s != 0 && 'mt-10']">
		<div class="text-center col-start-1 col-end-13 row-start-1">
			<div class="flex items-center text-gray-900">
				<p class="flex-auto font-semibold">
					{{ t(cal.monthString) + ", " + cal.yearString }}
				</p>
			</div>
			<div class="mt-6 grid grid-cols-7 text-xs leading-6 text-gray-500">
				<div>{{ t("weekday.abr.sunday") }}</div>
				<div>{{ t("weekday.abr.monday") }}</div>
				<div>{{ t("weekday.abr.tuesday") }}</div>
				<div>{{ t("weekday.abr.wednesday") }}</div>
				<div>{{ t("weekday.abr.thursday") }}</div>
				<div>{{ t("weekday.abr.friday") }}</div>
				<div>{{ t("weekday.abr.saturday") }}</div>
			</div>
			<div
				class="isolate mt-2 grid grid-cols-7 gap-px rounded-lg bg-black text-sm shadow ring-1 ring-black select-none">
				<div
					v-for="i of cal.monthdays.before"
					:key="i"
					:class="[
						`py-1.5 hover:bg-${hasHover(
							new Date(
								cal.cal.prev.getFullYear(),
								cal.cal.prev.getMonth(),
								cal.cal.prev.days - cal.cal.selected.firstDay + i
							)
						)} text-gray-400 bg-${hasBackground(
							new Date(
								cal.cal.prev.getFullYear(),
								cal.cal.prev.getMonth(),
								cal.cal.prev.days - cal.cal.selected.firstDay + i
							),
							true
						)}`,
						i == 1 && 'rounded-tl-lg',
						i == 7 && 'rounded-tr-lg',
					]">
					<p class="mx-auto flex h-7 w-7 items-center justify-center rounded-full">
						{{ cal.cal.prev.days - cal.cal.selected.firstDay + i }}
					</p>
				</div>
				<div
					v-for="(i, idx) of cal.monthdays.current"
					:key="i"
					:class="[
						`py-1.5 hover:bg-${hasHover(
							new Date(cal.cal.selected.year, cal.cal.selected.month, i)
						)} text-gray-900 group bg-${hasBackground(
							new Date(cal.cal.selected.year, cal.cal.selected.month, i),
							false
						)}`,
						i == cal.cal.today.getDate() &&
							cal.cal.selected.month == cal.cal.today.month &&
							cal.cal.selected.year == cal.cal.today.year &&
							'font-semibold bg-sky-200 hover:bg-sky-300',
						idx == 6 - cal.monthdays.before &&
							cal.monthdays.before < 7 &&
							'rounded-tr-lg',
						(idx + cal.monthdays.before) % 7 == 0 &&
							idx + 7 > cal.monthdays.current &&
							'rounded-bl-lg',
						cal.monthdays.after == 0 &&
							idx + 1 == cal.monthdays.current &&
							'rounded-br-lg',
						(Math.floor((idx + cal.cal.selected.firstDay) % 7) == 0 &&
							Math.floor((cal.cal.selected.days - idx) / 7) == 0) ||
							(Math.floor((cal.cal.selected.days - idx) / 7) == 1 &&
								cal.cal.selected.days - idx == 7 &&
								cal.monthdays.after == 0 &&
								'rounded-bl-lg'),
					]">
					<Tooltip
						:show="isEventDay(i, cal.cal)"
						:text="
							events.find(
								(a) =>
									a.date.getTime() ==
									new Date(
										cal.cal.selected.year,
										cal.cal.selected.month,
										i
									).getTime()
							)?.title + ''
						">
						<p
							:class="[
								'mx-auto flex h-7 w-7 items-center justify-center rounded-full',
								isEventDay(i, cal.cal) &&
									`font-bold cursor-pointer rounded-full relative bg-${
										events.find(
											(a) =>
												a.date.getTime() ==
												new Date(
													cal.cal.selected.year,
													cal.cal.selected.month,
													i
												).getTime()
										)?.color
									}`,
							]">
							{{ i }}
						</p>
					</Tooltip>
				</div>
				<div
					v-for="(i, idx) of cal.monthdays.after"
					:key="i"
					:class="[
						`py-1.5 hover:bg-${hasHover(
							new Date(cal.cal.after.getFullYear(), cal.cal.after.getMonth(), i)
						)}  text-gray-400 bg-${hasBackground(
							new Date(cal.cal.after.getFullYear(), cal.cal.after.getMonth(), i),
							true
						)}`,
						idx == cal.monthdays.after - 1 && 'rounded-br-lg',
					]">
					<p class="mx-auto flex h-7 w-7 items-center justify-center rounded-full">
						{{ i }}
					</p>
				</div>
			</div>
		</div>
	</div>
</template>

<script setup>
import Tooltip from "@/components/partials/templates/tooltip.vue";
import { ref, watch } from "vue";
import { useI18n } from "vue-i18n";

let { t } = useI18n();
const emit = defineEmits(["updateEnd"]);

const props = defineProps({
	// Array of objects with the events, example format {"date": new Date(2000, 1, 1), "title": "Title", "color": "red-500"}
	events: {
		type: Array,
		required: true,
		default: () => {
			return [];
		},
	},
	// Array of objects with the start dates for fill the background of the day, example format {"date": new Date(2000, 1, 1), "title": "Title", "color": "red"}
	start: {
		type: Array,
		required: true,
	},
	// Array of objects with the end dates for fill the background of the day, example format {"date": new Date(2000, 1, 1)}
	end: {
		type: Array,
		required: true,
	},
	// When update becomes true it update the calendar with the new start/end values
	update: {
		type: Boolean,
		required: false,
		default: false,
	},
});

let events = ref(props.events);
let startArray = ref([]);
let endArray = ref([]);
watch(
	() => props.events,
	(after) => {
		events.value = after;
		createCalendar();
	}
);
watch(
	() => props.update,
	() => {
		if (props.update) {
			createCalendar();
			emit("updateEnd");
		}
	}
);

let months = [
	"months.jan",
	"months.feb",
	"months.mar",
	"months.apr",
	"months.may",
	"months.jun",
	"months.jul",
	"months.aug",
	"months.sep",
	"months.oct",
	"months.nov",
	"months.dec",
];

let calendars = ref([]);

let Calendar = function (calendarEvents, date) {
	this.calendarEvents = calendarEvents;
	this.today = new Date();

	this.selected = this.today;
	this.today.month = this.today.getMonth();
	this.today.year = this.today.getFullYear();
	if (date) {
		this.selected = date;
	}
	this.selected.month = this.selected.getMonth();
	this.selected.year = this.selected.getFullYear();

	this.selected.days = new Date(this.selected.year, this.selected.month + 1, 0).getDate();
	this.selected.firstDay = new Date(this.selected.year, this.selected.month, 1).getDay();
	this.selected.lastDay = new Date(this.selected.year, this.selected.month + 1, 0).getDay();

	this.prev = new Date(this.selected.year, this.selected.month - 1, 1);
	if (this.selected.month == 0) {
		this.prev = new Date(this.selected.year - 1, 11, 1);
	}
	this.after = new Date(this.selected.year, this.selected.month + 1, 1);
	if (this.selected.month == 11) {
		this.prev = new Date(this.selected.year + 1, 0, 1);
	}
	this.prev.days = new Date(this.prev.getFullYear(), this.prev.getMonth() + 1, 0).getDate();
};

function createCalendar() {
	let eventsOrdered = [...props.events].sort((a, b) => a - b);
	let start = [...props.start].sort((a, b) => a.date - b.date);
	let end = [...props.end].sort((a, b) => b.date - a.date);
	let today = new Date();

	let lengthEvents = props.events.length;
	let lengthStart = props.start.length;
	let lengthEnd = props.end.length;
	if (lengthStart != lengthEnd) {
		return;
	}
	if (!orderDates()) {
		return;
	}
	calendars.value = [];

	let firstMonth =
		lengthStart == 0
			? lengthEvents == 0
				? today.getMonth()
				: eventsOrdered[0].date.getMonth()
			: lengthEvents == 0
			? start[0].date.getMonth()
			: eventsOrdered[0].date < start[0].date
			? eventsOrdered[0].date.getMonth()
			: start[0].date.getMonth();

	let firstYear =
		lengthStart == 0
			? lengthEvents == 0
				? today.getFullYear()
				: eventsOrdered[0].date.getFullYear()
			: lengthEvents == 0
			? start[0].date.getFullYear()
			: eventsOrdered[0].date < start[0].date
			? eventsOrdered[0].date.getFullYear()
			: start[0].date.getFullYear();

	eventsOrdered.sort((a, b) => b - a);
	let lastMonth =
		lengthEnd == 0
			? lengthEvents == 0
				? today.getMonth()
				: eventsOrdered[0].date.getMonth()
			: lengthEvents == 0
			? end[0].date.getMonth()
			: eventsOrdered[0].date < end[0].date
			? eventsOrdered[0].date.getMonth()
			: end[0].date.getMonth();
	let lastYear =
		lengthEnd == 0
			? lengthEvents == 0
				? today.getFullYear()
				: eventsOrdered[0].date.getFullYear()
			: lengthEvents == 0
			? end[0].date.getFullYear()
			: eventsOrdered[0].date < end[0].date
			? eventsOrdered[0].date.getFullYear()
			: end[0].date.getFullYear();
	for (let i = 0; i <= lastMonth + 12 * (lastYear - firstYear) - firstMonth; i++) {
		let auxCal = {
			cal: null,
			month: "",
			monthdays: {
				before: "",
				current: "",
				after: "",
			},
		};
		auxCal.cal = new Calendar(events.value, new Date(firstYear, firstMonth + i, 1));

		auxCal.monthString = months[auxCal.cal.selected.month];
		auxCal.yearString = auxCal.cal.selected.year;

		auxCal.monthdays.before = auxCal.cal.selected.firstDay;
		auxCal.monthdays.current = auxCal.cal.selected.days;
		auxCal.monthdays.after = 6 - auxCal.cal.selected.lastDay;

		calendars.value.push(auxCal);
	}
}

function orderDates() {
	for (let i = 0; i < props.start.length; i++) {
		let thisExists = false;
		for (let j = 0; j < props.start.length; j++) {
			if (props.start[i].color === props.end[j].color) {
				thisExists = true;
				break;
			}
		}
		if (!thisExists) {
			return false;
		}
	}
	startArray.value = [...props.start].sort((a, b) => a.color - b.color);
	endArray.value = [...props.end].sort((a, b) => a.color - b.color);
	return true;
}

function isEventDay(day, calendar) {
	for (let n = 0; n < calendar.calendarEvents.length; n++) {
		if (
			calendar.calendarEvents[n].date.getTime() ==
			new Date(calendar.selected.year, calendar.selected.month, day).getTime()
		) {
			return true;
		}
	}
	return false;
}

function hasBackground(date, soft) {
	let start = startArray.value;
	let end = endArray.value;
	if (start.length != end.length) {
		return "white";
	}
	for (let i = 0; i < start.length; i++) {
		if (date >= start[i].date && date <= end[i].date) {
			if (soft) {
				return start[i].color + "-100";
			}
			return start[i].color + "-200";
		}
	}
	if (soft) {
		return "gray-100";
	}
	return "white";
}

function hasHover(date) {
	let start = startArray.value;
	let end = endArray.value;
	if (start.length != end.length) {
		return "gray-200";
	}
	for (let i = 0; i < start.length; i++) {
		if (date >= start[i].date && date <= end[i].date) {
			return start[i].color + "-300";
		}
	}
	return "gray-200";
}

createCalendar();
</script>

<i18n>
{
  	"en_GB": {
		"previous": "Previous month",
		"next": "Next month",
		"header": "Delete {type}",
		"text": "Once you delete the {type}, you will lose all data associated with it.",
		"back": "Back",
		"btn": "Delete {type}",
		"weekday": {
			"abr": {
				"sunday": "S",
				"monday": "M",
				"tuesday": "T",
				"wednesday": "W",
				"thursday": "T",
				"friday": "F",
				"saturday": "S"
			}
		},
		"months": {
			"jan": "January",
			"feb": "February",
			"mar": "March",
			"apr": "April",
			"may": "May",
			"jun": "June",
			"jul": "July",
			"aug": "August",
			"sep": "September",
			"oct": "October",
			"nov": "November",
			"dec": "December"
		}
	},
  	"pt_PT": {
		"previous": "Mês anterior",
		"next": "Próximo mês",
		"header": "Apagar {type}",
		"text": "Assim que apagar a {type}, irá perder todos os dados associados a ela.",
		"back": "Voltar",
		"btn": "Apagar {type}",
		"weekday": {
			"abr": {
				"sunday": "D",
				"monday": "S",
				"tuesday": "T",
				"wednesday": "Q",
				"thursday": "Q",
				"friday": "S",
				"saturday": "S"
			}
		},
		"months": {
			"jan": "Janeiro",
			"feb": "Fevereiro",
			"mar": "Março",
			"apr": "Abril",
			"may": "Maio",
			"jun": "Junho",
			"jul": "Julho",
			"aug": "Agosto",
			"sep": "Setembro",
			"oct": "Outubro",
			"nov": "Novembro",
			"dec": "Dezembro"
		}
	},
}
</i18n>
