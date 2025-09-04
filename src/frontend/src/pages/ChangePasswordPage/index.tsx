import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../../contexts/authContext';
import { api } from '../../controllers/API/api';

interface ChangePasswordPageProps {}

const ChangePasswordPage: React.FC<ChangePasswordPageProps> = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { user, login } = useAuth();
  
  const [currentPassword, setCurrentPassword] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [isFromReset, setIsFromReset] = useState(false);

  // Check if user came from password reset
  useEffect(() => {
    const fromReset = searchParams.get('from_reset');
    if (fromReset === 'true') {
      setIsFromReset(true);
    }
  }, [searchParams]);

  const validatePassword = (password: string): string[] => {
    const errors: string[] = [];
    
    if (password.length < 8) {
      errors.push('Lösenordet måste vara minst 8 tecken långt');
    }

    if (!/[A-Z]/.test(password)) {
      errors.push('Lösenordet måste innehålla minst en stor bokstav');
    }

    if (!/[a-z]/.test(password)) {
      errors.push('Lösenordet måste innehålla minst en liten bokstav');
    }

    if (!/\d/.test(password)) {
      errors.push('Lösenordet måste innehålla minst en siffra');
    }

    if (!/[!@#$%^&*(),.?":{}|<>]/.test(password)) {
      errors.push('Lösenordet måste innehålla minst ett specialtecken');
    }
    
    return errors;
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    // Validate new password
    const passwordErrors = validatePassword(newPassword);
    if (passwordErrors.length > 0) {
      setError(passwordErrors.join('. '));
      return;
    }

    // Check if passwords match
    if (newPassword !== confirmPassword) {
      setError('Nya lösenorden stämmer inte överens');
      return;
    }

    // If not from reset, require current password
    if (!isFromReset && !currentPassword.trim()) {
      setError('Nuvarande lösenord krävs');
      return;
    }

    setIsLoading(true);

    try {
      const payload = {
        new_password: newPassword,
        ...(isFromReset ? {} : { current_password: currentPassword })
      };

      const response = await api.post('/api/v1/auth/change-password', payload);

      if (response.data.success) {
        setSuccess('Lösenordet ändrades framgångsrikt! Du kommer att omdirigeras till din instrumentpanel.');
        
        // Clear form
        setCurrentPassword('');
        setNewPassword('');
        setConfirmPassword('');
        
        // Redirect after 2 seconds
        setTimeout(() => {
          navigate('/dashboard');
        }, 2000);
      } else {
        setError(response.data.message || 'Misslyckades att ändra lösenord');
      }
    } catch (error: any) {
      console.error('Change password error:', error);
      
      if (error.response?.status === 400) {
        setError(error.response.data.detail || 'Ogiltiga lösenordskrav');
      } else if (error.response?.status === 401) {
        setError('Nuvarande lösenord är felaktigt');
      } else if (error.response?.status === 422) {
        setError('Lösenordsvalidering misslyckades. Vänligen kontrollera kraven.');
      } else {
        setError('Misslyckades att ändra lösenord. Vänligen försök igen.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="bg-white rounded-xl shadow-lg p-8">
          {/* Header */}
          <div className="text-center mb-8">
            <img
              src="/logo192.png"
              alt="Axie Studio logo"
              className="mx-auto h-16 w-16 rounded-xl object-contain mb-4"
              onError={(e) => {
                // Fallback to text logo if image fails to load
                e.currentTarget.style.display = 'none';
                e.currentTarget.nextElementSibling.style.display = 'flex';
              }}
            />
            <div className="mx-auto h-16 w-16 bg-primary text-primary-foreground rounded-xl items-center justify-center mb-4 font-bold text-xl hidden">
              AS
            </div>
            <h2 className="text-3xl font-bold text-gray-900">
              {isFromReset ? 'Ange Nytt Lösenord' : 'Ändra Lösenord'}
            </h2>
            <p className="mt-2 text-sm text-gray-600">
              {isFromReset
                ? 'Skapa ett starkt lösenord för ditt konto'
                : 'Uppdatera ditt kontolösenord'
              }
            </p>
          </div>

          {/* Success Message */}
          {success && (
            <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <p className="text-sm font-medium text-green-800">{success}</p>
                </div>
              </div>
            </div>
          )}

          {/* Error Message */}
          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg">
              <div className="flex">
                <div className="flex-shrink-0">
                  <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                  </svg>
                </div>
                <div className="ml-3">
                  <p className="text-sm font-medium text-red-800">{error}</p>
                </div>
              </div>
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Current Password (only if not from reset) */}
            {!isFromReset && (
              <div>
                <label htmlFor="current-password" className="block text-sm font-medium text-gray-700 mb-2">
                  Nuvarande Lösenord
                </label>
                <input
                  id="current-password"
                  name="current-password"
                  type="password"
                  value={currentPassword}
                  onChange={(e) => setCurrentPassword(e.target.value)}
                  required={!isFromReset}
                  disabled={isLoading}
                  className="appearance-none relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                  placeholder="Ange ditt nuvarande lösenord"
                />
              </div>
            )}

            {/* New Password */}
            <div>
              <label htmlFor="new-password" className="block text-sm font-medium text-gray-700 mb-2">
                Nytt Lösenord
              </label>
              <input
                id="new-password"
                name="new-password"
                type="password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                required
                disabled={isLoading}
                className="appearance-none relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                placeholder="Ange ditt nya lösenord"
              />
            </div>

            {/* Confirm New Password */}
            <div>
              <label htmlFor="confirm-password" className="block text-sm font-medium text-gray-700 mb-2">
                Bekräfta Nytt Lösenord
              </label>
              <input
                id="confirm-password"
                name="confirm-password"
                type="password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                required
                disabled={isLoading}
                className="appearance-none relative block w-full px-3 py-3 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
                placeholder="Bekräfta ditt nya lösenord"
              />
            </div>

            {/* Password Requirements */}
            <div className="bg-gray-50 rounded-lg p-4">
              <h4 className="text-sm font-medium text-gray-700 mb-2">Lösenordskrav:</h4>
              <ul className="text-xs text-gray-600 space-y-1">
                <li>• Minst 8 tecken långt</li>
                <li>• Innehåller stora och små bokstäver</li>
                <li>• Innehåller minst en siffra</li>
                <li>• Innehåller minst ett specialtecken</li>
              </ul>
            </div>

            {/* Submit Button */}
            <div>
              <button
                type="submit"
                disabled={isLoading}
                className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
              >
                {isLoading ? (
                  <div className="flex items-center">
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                    Ändrar Lösenord...
                  </div>
                ) : (
                  'Ändra Lösenord'
                )}
              </button>
            </div>
          </form>

          {/* Footer */}
          <div className="mt-6 text-center">
            <button
              onClick={() => navigate('/dashboard')}
              className="text-sm text-blue-600 hover:text-blue-500 font-medium"
            >
              Tillbaka till Instrumentpanel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ChangePasswordPage;
