// Copyright (c) Jupyter Development Team.
// Distributed under the terms of the Modified BSD License.

// Add any needed widget imports here (or from controls)
// import {} from '@jupyter-widgets/base';

import { createTestModel } from './utils';
import { MsalWidgetModel } from '..';

describe('Example', () => {
  describe('ExampleModel', () => {
    it('should be createable', () => {
      const model = createTestModel(MsalWidgetModel);
      expect(model).toBeInstanceOf(MsalWidgetModel);
      expect(model.get('signed_in')).toEqual(false);
    });

    it('should be createable with a value', () => {
      const state = { signed_in: true };
      const model = createTestModel(MsalWidgetModel, state);
      expect(model).toBeInstanceOf(MsalWidgetModel);
      expect(model.get('signed_in')).toEqual(true);
    });
  });
});
