import joblib, os
import warnings
warnings.filterwarnings('ignore')
PACKAGE_DIR = os.path.dirname(__file__)

class TextClassifier(object):
    def __init__(self, text=None):
        super(TextClassifier, self).__init__()
        self.text = text

    def __repr__(self):
        return "TextClassifier(text={})".format(self.text)

    def predict(self):
        spam_vectorizer = open(os.path.join(PACKAGE_DIR, "models/spam_vectorizer.pkl"), "rb")
        spam_cv = joblib.load(spam_vectorizer)

        spam_detector_nv_model = open(os.path.join(PACKAGE_DIR, "models/spam_detector_nb_model.pkl"), "rb")
        spam_detector_clf = joblib.load(spam_detector_nv_model)

        vectorized_text = spam_cv.transform([self.text]).toarray()
        prediction = spam_detector_clf.predict(vectorized_text)

        if prediction[0] == 0:
            prediction = 'Not Spam'
        elif prediction[0] == 1:
            prediction = 'Is Spam'

        return prediction


    def load_model(self, model_type):
        if model_type == 'nv':
            nv_model = open(os.path.join(PACKAGE_DIR, "models/spam_detector_nb_model.pkl"), "rb")
            spam_detector_clf = joblib.load(nv_model)
        elif model_type == 'logit':
            logit_model = open(os.path.join(PACKAGE_DIR, "models/spam_detector_logit_model.pkl"), "rb")
            spam_detector_clf = joblib.load(logit_model)
        elif model_type == 'rf':
            rf_model = open(os.path.join(PACKAGE_DIR, "models/spam_detector_rf_model.pkl"), "rb")
            spam_detector_clf = joblib.load(rf_model)
        else:
            return 'Please enter correct model type [\'nv\': Naive Bayes, \'logit\': Logistic Regression, \'rf\': Random Forest]'

        return spam_detector_clf

    def classify(self, new_text=None):
        if new_text is not None:
            self.text = new_text
        prediction = self.predict()
        return prediction

    def is_spam(self, new_text=None):
        if new_text is not None:
            self.text = new_text
        prediction = self.predict()
        return bool(prediction=='Is Spam')