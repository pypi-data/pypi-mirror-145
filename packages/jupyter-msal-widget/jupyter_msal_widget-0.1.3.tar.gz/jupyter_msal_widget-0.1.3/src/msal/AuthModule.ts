import {
  PublicClientApplication,
  AuthenticationResult,
  Configuration,
  LogLevel,
  AccountInfo,
  PopupRequest,
  EndSessionRequest,
} from '@azure/msal-browser';

/**
 * Configuration class for @azure/msal-browser:
 * https://azuread.github.io/microsoft-authentication-library-for-js/ref/msal-browser/modules/_src_config_configuration_.html
 */
const BASE_MSAL_CONFIG: Configuration = {
  auth: { clientId: '' },
  cache: {
    cacheLocation: 'sessionStorage', // This configures where your cache will be stored
    storeAuthStateInCookie: false, // Set this to "true" if you are having issues on IE11 or Edge
  },
  system: {
    loggerOptions: {
      loggerCallback: (level: any, message: any, containsPii: any) => {
        if (containsPii) {
          return;
        }
        switch (level) {
          case LogLevel.Error:
            console.error(message);
            return;
          case LogLevel.Info:
            console.info(message);
            return;
          case LogLevel.Verbose:
            console.debug(message);
            return;
          case LogLevel.Warning:
            console.warn(message);
            return;
        }
      },
    },
  },
};

/**
 * AuthModule for application - handles authentication in app.
 */
export class AuthModule {
  private myMSALObj: PublicClientApplication; // https://azuread.github.io/microsoft-authentication-library-for-js/ref/msal-browser/classes/_src_app_publicclientapplication_.publicclientapplication.html
  public account: AccountInfo | null; // https://azuread.github.io/microsoft-authentication-library-for-js/ref/msal-common/modules/_src_account_accountinfo_.html
  private loginRequest: PopupRequest; // https://azuread.github.io/microsoft-authentication-library-for-js/ref/msal-browser/modules/_src_request_popuprequest_.html

  constructor(args: { clientId: string; authority: string | undefined }) {
    const msal_config = BASE_MSAL_CONFIG;
    msal_config.auth.clientId = args.clientId;
    msal_config.auth.authority = args.authority;
    this.myMSALObj = new PublicClientApplication(msal_config);
    this.account = null;

    this.loginRequest = { scopes: [] };
  }

  public getAccount(): AccountInfo | null {
    // need to call getAccount here?
    const currentAccounts = this.myMSALObj.getAllAccounts();
    if (currentAccounts === null) {
      console.log('No accounts detected');
      return null;
    }

    if (currentAccounts.length > 1) {
      // Add choose account code here
      console.log(
        'Multiple accounts detected, need to add choose account code.'
      );
      return currentAccounts[0];
    } else if (currentAccounts.length === 1) {
      return currentAccounts[0];
    }

    return null;
  }

  /**
   * Checks whether we are in the middle of a redirect and handles state accordingly. Only required for redirect flows.
   *
   * https://github.com/AzureAD/microsoft-authentication-library-for-js/blob/dev/lib/msal-browser/docs/initialization.md#redirect-apis
   */
  loadAuthModule(): void {
    this.myMSALObj
      .handleRedirectPromise()
      .then((resp: AuthenticationResult | null) => {
        // this.handleResponse(resp);
      })
      .catch(console.error);
  }

  // /**
  //  * Handles the response from a popup or redirect. If response is null, will check if we have any accounts and attempt to sign in.
  //  * @param response
  //  */
  // // eslint-disable-next-line @typescript-eslint/explicit-module-boundary-types
  // handleResponse(response: AuthenticationResult | null) {
  //   if (response !== null) {
  //     this.account = response.account;
  //   } else {
  //     this.account = this.getAccount();
  //   }
  // }

  /**
   * Callback after the response
   * @param callback
   */
  // eslint-disable-next-line @typescript-eslint/ban-types
  login(callback?: (value: void) => void): void {
    this.myMSALObj
      .loginPopup(this.loginRequest)
      // .then(this.handleResponse)
      .then((data: any) => {
        if (callback) {
          callback(data);
        }
        return data;
      })
      .catch(console.error);
  }

  /**
   * Logs out of current account.
   */
  logout(callback?: (value: void) => void): void {
    let account: AccountInfo | undefined;
    if (this.account) {
      account = this.account;
    }
    const logOutRequest: EndSessionRequest = { account };

    this.myMSALObj.logoutPopup(logOutRequest).then((data: any) => {
      if (callback) {
        callback(data);
      }
      return data;
    });
  }
}
