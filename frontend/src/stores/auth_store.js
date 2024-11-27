import { ref, computed } from 'vue';
import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', () => {
    const backend_server = 'http://127.0.0.1:5000/api/iescp2'; // Defining  backend server URL

    const token = ref(localStorage.getItem('auth_token'));
    const user_details = ref(localStorage.getItem('user_details'));

    const isAuthenticated = computed(() => {
        return token.value !== null
    });

    const userRoles = computed(() => {
        const user = user_details.value ? JSON.parse(user_details.value) : null;
        return user?.roles || [];
    });

    function getAuthToken() {
        return token.value;
    }

    function getUserDetails() {
        try {
            return user_details.value;
        } catch (error) {
            console.error('Error parsing user details:', error);
            return null; // Return null if parsing fails
        }
    }
    
    function setAuthToken(new_token) {
        token.value = new_token;
        localStorage.setItem('auth_token', new_token);
    }

    function setUserDetails(new_user_details) {
        user_details.value = JSON.stringify(new_user_details); // Store as string in the reactive ref
        localStorage.setItem('user_details', JSON.stringify(new_user_details)); // Update localStorage
        console.log('Updated user_details:', new_user_details); // Debugging log
    }
    
    function removeAuthenticatedUser() {
        localStorage.removeItem('auth_token');
        localStorage.removeItem('user_details');
        token.value = null;
        user_details.value = null;
    }

    function getBackendServerURL() {
        return backend_server;
    }

 

    async function login(email, password, role) {
        try {
            console.log('Payload:', { email, password, role }); // Debugging
            const response = await fetch(`${getBackendServerURL()}/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ email, password, role }),
            });
    
            const data = await response.json();
            console.log('Login Response:', data)
    
            if (response.ok) {
                setAuthToken(data.login_credentials.auth_token);
                setUserDetails({
                    username: data.login_credentials.username,
                    roles: data.login_credentials.roles,
                });
                console.log('Token and User Details Set:', {
                    token: data.login_credentials.auth_token,
                    user: {
                        username: data.login_credentials.username,
                        roles: data.login_credentials.roles,
                    },
                });
                return data;
            } else {
                throw new Error(data.message || 'Login failed');
            }
        } catch (error) {
            console.error('Login failed:', error);
            throw error;
        }
    }
    
    

    async function logout() {
        try {
            await fetch(`${getBackendServerURL()}/logout`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authentication-Token': token.value,
                },
            });
            removeAuthenticatedUser();
        } catch (error) {
            console.error('Logout failed:', error);
        }
    }

    function hasRole(role) {
        return userRoles.value.includes(role);
    }

    function isAdmin() {
        return hasRole('admin');
    }

    function isSponsor() {
        return hasRole('sponsor');
    }

    function isInfluencer() {
        return hasRole('influencer');
    }

    return {
        getBackendServerURL, // Include this in the returned object
        isAuthenticated,
        getAuthToken,
        getUserDetails,
        setAuthToken,
        setUserDetails,
        removeAuthenticatedUser,
        login,
        logout,
        userRoles,
        isAdmin,
        isSponsor,
        isInfluencer,
    };
});
