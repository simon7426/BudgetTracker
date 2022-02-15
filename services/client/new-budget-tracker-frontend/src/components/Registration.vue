<template>
    <div class="col-md-12">
        <div class="card card-container">
            <img 
                id="profile-img" 
                src="//ssl.gstatic.com/accounts/ui/avatar_2x.png" 
                alt="register-profile" 
            />
            <Form @submit="handleRegister" :validation-schema="schema">
                <div v-if="!successful">
                    <div class="form-group">
                        <label for="username">Username</label>
                        <Field name="username" type="text" class="form-control" />
                        <ErrorMessage name="username" class="error-feedback" />
                    </div>
                    <div class="form-group">
                        <label for="account_name">Email/Phone No</label>
                        <Field name="account_name" type="text" class="form-control" />
                        <ErrorMessage name="account_name" class="error-feedback" />
                    </div>
                    <div class="form-group">
                        <label for="password">Username</label>
                        <Field name="password" type="password" class="form-control" />
                        <ErrorMessage name="password" class="error-feedback" />
                    </div>
                    <div class="form-group">
                        <button class="btn btn-primary btn-block" :disabled="loading">
                            <span v-show="loading" class="spinner-border spinner-border-sm"></span>
                            Sign Up
                        </button>
                    </div>
                </div>
            </Form>
            <div
                v-if="message"
                class="alert"
                :class="successful ? 'alert-success' : 'alert-danger'">
                {{ message }}
            </div>
        </div>
    </div>
</template>
<script>
import { Form, Field, ErrorMessage } from "vee-validate";
import * as yup from "yup";
export default {
    name: "Resgister",
    components: {
        Form,
        Field,
        ErrorMessage,
    },
    data() {
        const schema = yup.object().shape({
            username: yup
                .string()
                .required("Username is required!"),
            account_name: yup
                .string()
                .required("Email or Phone number is required!"),
            password: yup
                .string()
                .required("Password is required")
                .min(6, "Must be at least 6 characters!")
        });
        return {
            successful: false,
            loading: false,
            message: "",
            schema,
        };
    },
    computed: {
        loggedIn() {
            return this.$store.state.auth.status.loggedIn;
        },
    },
    mounted() {
        if (this.loggedIn) {
            this.$router.push("/profile")
        }
    },
    methods: {
        handleRegister(user) {
            this.message = "";
            this.successful = "";
            this.loading = true;
            this.$store.dispatch("auth/register", user).then(
                (data) => {
                    this.message = data.message;
                    this.successful = true;
                    this.loading = false;
                },
                (error) => {
                    this.message = (
                        error.response &&
                        error.response.data &&
                        error.response.data.message
                    ) || 
                    error.message ||
                    error.toString();
                    this.successful = false;
                    this.loading = false;
                }
            );
        },
    }
};
</script>
<style scoped>

</style>