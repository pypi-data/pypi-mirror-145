/* eslint-disable @typescript-eslint/ban-ts-comment */
/* eslint-disable @typescript-eslint/explicit-module-boundary-types */
// Copyright (c) Felipe Oucharski
// Distributed under the terms of the Modified BSD License.
import _ from 'lodash';
import { Promise as BBPromise } from 'bluebird';

import {
  DOMWidgetModel,
  DOMWidgetView,
  WidgetModel,
  unpack_models,
  ISerializers,
} from '@jupyter-widgets/base';

// import * as managerBase from '@jupyter-widgets/base';

import { MODULE_NAME, MODULE_VERSION } from './version';

// Import the CSS
import '../css/widget.css';
import { ViewOptions } from 'backbone';
import { AuthModule } from './msal';
import { labels } from './settings';

export class MsalWidgetModel extends DOMWidgetModel {
  defaults() {
    return {
      ...super.defaults(),
      _model_name: MsalWidgetModel.model_name,
      _model_module: MsalWidgetModel.model_module,
      _model_module_version: MsalWidgetModel.model_module_version,
      _view_name: MsalWidgetModel.view_name,
      _view_module: MsalWidgetModel.view_module,
      _view_module_version: MsalWidgetModel.view_module_version,
      content: undefined,
      signed_in: false,
    };
  }

  static serializers: ISerializers = {
    ...DOMWidgetModel.serializers,
    // @ts-ignore
    content: { deserialize: unpack_models },
  };

  static model_name = 'MsalWidgetModel';
  static model_module = MODULE_NAME;
  static model_module_version = MODULE_VERSION;
  static view_name = 'MsalWidgetView';
  static view_module = MODULE_NAME;
  static view_module_version = MODULE_VERSION;
}

type MsalWidgetViewArgs =
  | (ViewOptions<WidgetModel, HTMLElement> & { options?: any })
  | undefined;

export class MsalWidgetView extends DOMWidgetView {
  private _button: HTMLButtonElement;
  private _authModule: AuthModule;
  private displayLogout: boolean;
  private content: any;

  createAuthModule = () => {
    const clientId = this.model.get('client_id');
    const authority = this.model.get('authority_url');
    this._authModule = new AuthModule({ clientId, authority });
  };

  getSignedIn = (): [boolean, any] => {
    const account = this._authModule.getAccount() || {};
    const signed_in = !_.isEmpty(account);
    return [signed_in, account];
  };

  setContent = async () => {
    if (!this.content) {
      await BBPromise.props({
        content: this.create_child_view(this.model.get('content')),
      }).then((childrenViews) => {
        this.content = childrenViews.content;
      });
    }
  };

  modifyStyle = () => {
    document.documentElement.style.setProperty(
      '--button-main-color',
      this.model.get('button_main_color')
    );

    css(this._button, this.model.get('button_style'));
  };

  constructor(args: MsalWidgetViewArgs) {
    super(args);
    this.createAuthModule();
    this.handleBackendChanges();
  }

  async render() {
    this.displayLogout = this.model.get('display_logout');

    await this.setContent();
    this.buildFrontend();
    this.handleFrontendChanges();
    this.model.on('change:signed_in', this.onBackendChanges, this);
  }

  onBackendChanges = async () => {
    await this.handleFrontendChanges();
  };

  handleBackendChanges = () => {
    const [signed_in, account] = this.getSignedIn();
    this.model.set({ account, signed_in });
    this.touch();
  };

  buildFrontend = () => {
    // BUTTON
    this._button = document.createElement('button');
    this._button.classList.add('button');
    this._button.onclick = this.onClick;

    // PARENT
    this.el.appendChild(this._button);
    this.el.classList.add('widget-container');

    this.modifyStyle();
  };

  handleFrontendChanges = async () => {
    const [signed_in] = this.getSignedIn();

    if (signed_in) {
      this._button.innerHTML = labels.logoff;
      if (this.displayLogout) {
        toggleElement(this.el, this._button, true);
      } else {
        toggleElement(this.el, this._button, false);
      }

      toggleElement(this.el, this.content.el, true);
    } else {
      this._button.innerHTML = labels.login;

      toggleElement(this.el, this.content.el, false);
    }
  };

  onClick = () => {
    const [signed_in] = this.getSignedIn();
    (signed_in && this._authModule.logout(this.handleBackendChanges)) ||
      this._authModule.login(this.handleBackendChanges);
  };
}

const toggleElement = (
  container: {
    contains: (arg0: any) => any;
    removeChild: (arg0: any) => void;
    appendChild: (arg0: any) => void;
  },
  element: any,
  add: any
) => {
  const contains = container.contains(element);

  if (contains && !add) {
    container.removeChild(element);
  }

  if (!contains && add) {
    container.appendChild(element);
  }
};

const css = (
  element: { style: { [x: string]: any } },
  style: { [x: string]: any }
) => {
  if (element) {
    for (const property in style) {
      element.style[property] = style[property];
    }
  }
};
