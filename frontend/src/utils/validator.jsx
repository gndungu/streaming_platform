export const validateForm = (form) => {
  const errors = {};

  const usernameRegex = /^[a-zA-Z][a-zA-Z0-9_]{2,19}$/;

  if (!form.username) {
    errors.username = "Username is required";
  } 
//   else if (!usernameRegex.test(form.username)) {
//     errors.username =
//       "Username must be 3–20 chars, start with letter, only letters/numbers/_";
//   }

  if (!form.password) {
    errors.password = "Password is required";
  } else if (form.password.length < 6) {
    errors.password = "Password must be at least 6 characters";
  }

  return errors;
};