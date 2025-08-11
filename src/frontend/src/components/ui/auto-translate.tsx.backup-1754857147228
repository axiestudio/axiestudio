import React from 'react';
import { /**
 * Auto-translation mapping for common UI strings
 * This allows automatic translation of hardcoded strings without manual component updates
 */
const TRANSLATION_MAP: Record<string, string> = {
  // Common actions
  'Save': 'common.save',
  'Cancel': 'common.cancel',
  'Delete': 'common.delete',
  'Edit': 'common.edit',
  'Add': 'common.add',
  'Close': 'common.close',
  'Confirm': 'common.confirm',
  'Yes': 'common.yes',
  'No': 'common.no',
  'Build': 'common.build',
  'Run': 'common.run',
  'Stop': 'common.stop',
  'Copy': 'common.copy',
  'Paste': 'common.paste',
  'Search': 'common.search',
  'Filter': 'common.filter',
  'Settings': 'common.settings',
  'Help': 'common.help',
  'Loading...': 'common.loading',
  
  // Navigation
  'My Collection': 'navigation.myCollection',
  'Axie Studio Store': 'navigation.store',
  'Admin Page': 'navigation.adminPage',
  'Playground': 'navigation.playground',
  
  // Sidebar components
  'Saved': 'sidebar.savedComponents',
  'Input / Output': 'sidebar.inputOutput',
  'Agents': 'sidebar.agents',
  'Models': 'sidebar.models',
  'Data': 'sidebar.data',
  'Vector Stores': 'sidebar.vectorStores',
  'Processing': 'sidebar.processing',
  'Logic': 'sidebar.logic',
  'Helpers': 'sidebar.helpers',
  'Inputs': 'sidebar.inputs',
  'Outputs': 'sidebar.outputs',
  
  // Flow status
  'Build to validate status.': 'flows.buildToValidate',
  'Please fill all the required fields.': 'flows.fillRequiredFields',
  'Execution blocked': 'flows.executionBlocked',
  'Building...': 'flows.building',
  'Built successfully ✨': 'flows.builtSuccessfully',
  
  // File management
  'Please select a valid file. Only these file types are allowed:': 'fileManagement.selectValidFile',
  'Error occurred while uploading file': 'fileManagement.fileUploadError',
  
  // Components
  'Your component is outdated. Click to update (data may be lost)': 'components.outdatedComponent',
  'Expand hidden outputs': 'components.expandHiddenOutputs',
  'Collapse hidden outputs': 'components.collapseHiddenOutputs',
  'Available input components:': 'components.availableInputComponents',
  'Available output components:': 'components.availableOutputComponents',
  
  // Messages
  'No input message provided.': 'messages.noInputMessage',
  'Message empty.': 'messages.emptyMessage',
  'Send a message...': 'messages.sendMessage',
  'Type message here.': 'messages.typeMessage',
  
  // Placeholders
  'Type something...': 'common.defaultPlaceholder',
  'Select an option': 'common.selectAnOption',
  'Used as a tool': 'common.defaultToolsetPlaceholder',
  'Receiving input': 'common.receivingInputValue',
  
  // Auth
  'Welcome to Axie Studio': 'auth.welcome',
  'Sign in to continue to your workspace': 'auth.signInSubtitle',
  'Username': 'auth.username',
  'Password': 'auth.password',
  'Sign in': 'auth.signIn',
  'Enter your username': 'auth.enterUsername',
  'Enter your password': 'auth.enterPassword',
  
  // Projects
  'Manage your projects. Download and upload entire collections.': 'projects.myCollectionDesc',
  'Explore community-shared flows and components.': 'projects.storeDesc',
  'Starter Project': 'projects.defaultFolder',
  
  // API
  'Your secret Axie Studio API keys are listed below. Do not share your API key with others, or expose it in the browser or other client-side code.': 'api.apiPageParagraph',
  'This user does not have any keys assigned at the moment.': 'api.apiPageUserKeys',
  'You don\'t have an API key.': 'api.noApiKey',
  'Insert your Axie Studio API key.': 'api.insertApiKey',
  'Your API key is not valid.': 'api.invalidApiKey',
  'API key saved successfully': 'api.saveApiKeyAlert',
  
  // Chat
  'Axie Studio Chat': 'chat.axiestudioChatTitle',
  'No chat input variables found. Click to run your flow.': 'chat.chatInputPlaceholder',
  'Start a conversation and click the agent\'s memories': 'chat.chatFirstInitialText',
  'to inspect previous messages.': 'chat.chatSecondInitialText',
  
  // Notifications
  'No new notifications': 'notifications.zeroNotifications'
 };

interface AutoTranslateProps {
  children: React.ReactNode;
  fallback?: string;
}

/**
 * Component that automatically translates common UI strings
 * Usage: <AutoTranslate>Save</AutoTranslate> → "Spara" in Swedish
 */
export function AutoTranslate({ children, fallback }: AutoTranslateProps) {
  const { t } = useTranslation();
  
  // Convert children to string for lookup
  const text = React.Children.toArray(children).join('');
  
  // Look up translation key
  const translationKey = TRANSLATION_MAP[text];
  
  if (translationKey) {
    return <>{t(translationKey)}</>;
  }
  
  // Return original text if no translation found
  return <>{fallback || children}</>;
}

/**
 * Hook to automatically translate text strings
 * Usage: const translatedText = useAutoTranslate('Save');
 */
export function useAutoTranslate() {
  const { t } = useTranslation();
  
  return (text: string): string => {
    const translationKey = TRANSLATION_MAP[text];
    return translationKey ? t(translationKey) : text;
  };
}

/**
 * Higher-order component that wraps text nodes with AutoTranslate
 * This can be used to automatically translate entire component trees
 */
export function withAutoTranslate<P extends object>(
  Component: React.ComponentType<P>
) {
  return function AutoTranslatedComponent(props: P) {
    return <Component {...props} />;
  };
}
