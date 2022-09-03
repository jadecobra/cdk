import jadecobra.toolkit
import src.well_architected_constructs


class TestApiLambda(jadecobra.toolkit.TestCase):

    def test_api_lambda(self):
        self.assert_attributes_equal(
            src.well_architected_constructs.api_lambda,
            sorted([
                '__builtins__',
                '__cached__',
                '__doc__',
                '__file__',
                '__loader__',
                '__name__',
                '__package__',
                '__spec__',
                'api',
                'aws_cdk',
                'create_http_api_lambda',
                'create_rest_api_lambda',
            ])
        )
