import { useToast } from "vue-toastification";

const toast = useToast();

const genericError = () => toast.error("Server error. Please try again later.");

/*
EXAMPLES OF TOASTS

toast("Default toast")
toast.info("Info toast")
toast.success("Success toast")
toast.error("Error toast")
toast.warning("Warning toast")
*/

export { toast as default, genericError };
