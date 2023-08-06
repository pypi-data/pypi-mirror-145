# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['datadog_lambda']

package_data = \
{'': ['*']}

install_requires = \
['datadog>=0.41.0,<0.42.0', 'ddtrace>=0.59.2,<0.60.0', 'wrapt>=1.11.2,<2.0.0']

extras_require = \
{':python_version < "3.8"': ['typing_extensions>=4.0,<5.0',
                             'importlib_metadata>=1.0,<2.0'],
 u'dev': ['nose2>=0.9.1,<0.10.0',
          'httpretty>=0.9.7,<0.10.0',
          'boto3>=1.10.33,<2.0.0',
          'requests>=2.22.0,<3.0.0',
          'flake8>=3.7.9,<4.0.0']}

setup_kwargs = {
    'name': 'datadog-lambda',
    'version': '3.56.0',
    'description': 'The Datadog AWS Lambda Library',
    'long_description': "# datadog-lambda-python\n\n![build](https://github.com/DataDog/datadog-lambda-python/workflows/build/badge.svg)\n[![PyPI](https://img.shields.io/pypi/v/datadog-lambda)](https://pypi.org/project/datadog-lambda/)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/datadog-lambda)\n[![Slack](https://chat.datadoghq.com/badge.svg?bg=632CA6)](https://chat.datadoghq.com/)\n[![License](https://img.shields.io/badge/license-Apache--2.0-blue)](https://github.com/DataDog/datadog-lambda-python/blob/main/LICENSE)\n\nDatadog Lambda Library for Python (3.6, 3.7, 3.8, and 3.9) enables [enhanced Lambda metrics](https://docs.datadoghq.com/serverless/enhanced_lambda_metrics), [distributed tracing](https://docs.datadoghq.com/serverless/distributed_tracing), and [custom metric submission](https://docs.datadoghq.com/serverless/custom_metrics) from AWS Lambda functions.\n\n## Installation\n\nFollow the [installation instructions](https://docs.datadoghq.com/serverless/installation/python/), and view your function's enhanced metrics, traces and logs in Datadog.\n\nFor advanced distributed tracing use cases, check out the [official documentation for Datadog APM client](https://ddtrace.readthedocs.io).\n\nTo connect traces and logs using a custom logger, see [connecting logs and traces](https://docs.datadoghq.com/tracing/connect_logs_and_traces/python/).\n\n## Environment Variables\n\n### DD_API_KEY\n\nIf you are using the [Datadog Lambda Extension](https://docs.datadoghq.com/serverless/libraries_integrations/extension/), the Datadog API Key must be defined by setting one of the following environment variables:\n\n- DD_API_KEY - the Datadog API Key in plain-text, NOT recommended\n- DD_KMS_API_KEY - the KMS-encrypted API Key, requires the `kms:Decrypt` permission\n- DD_API_KEY_SECRET_ARN - the Secret ARN to fetch API Key from the Secrets Manager, requires the `secretsmanager:GetSecretValue` permission (and `kms:Decrypt` if using a customer managed CMK)\n\nIf you are using the [Datadog Forwarder](https://github.com/DataDog/datadog-serverless-functions/tree/main/aws/logs_monitoring), you must set the Datadog API Key on the Datadog Forwarder instead of your own Lambda function.\n\n### DD_SITE\n\nIf you are using the [Datadog Lambda Extension](https://docs.datadoghq.com/serverless/libraries_integrations/extension/), you must set `DD_SITE` on your Lambda function based on your [Datadog site](https://docs.datadoghq.com/getting_started/site/). The default is `datadoghq.com`. \n\nIf you are using the [Datadog Forwarder](https://github.com/DataDog/datadog-serverless-functions/tree/main/aws/logs_monitoring), you must set this on the Datadog Forwarder instead of your own Lambda function.\n\n### DD_LOGS_INJECTION\n\nInject Datadog trace id into logs for [correlation](https://docs.datadoghq.com/tracing/connect_logs_and_traces/python/) if you are using a `logging.Formatter` in the default `LambdaLoggerHandler` by the Lambda runtime. Defaults to `true`.\n\n### DD_LOG_LEVEL\n\nSet to `debug` enable debug logs from the Datadog Lambda Library. Defaults to `info`.\n\n### DD_ENHANCED_METRICS\n\nGenerate enhanced Datadog Lambda integration metrics, such as, `aws.lambda.enhanced.invocations` and `aws.lambda.enhanced.errors`. Defaults to `true`.\n\n### DD_LAMBDA_HANDLER\n\nIn order to instrument individual invocations, the Datadog Lambda library needs to wrap around your Lambda handler function. This is usually achieved by setting your function's handler to the Datadog handler function (`datadog_lambda.handler.handler`) and setting the environment variable `DD_LAMBDA_HANDLER` with your original handler function to be called by the Datadog handler.\n\nFor some advanced use cases, instead of overriding the handler setting and the `DD_LAMBDA_HANDLER` environment variable, you can apply the Datadog Lambda library wrapper in your function code like below:\n\n```python\nfrom datadog_lambda.wrapper import datadog_lambda_wrapper\n\n@datadog_lambda_wrapper\ndef my_lambda_handle(event, context):\n    # your function code\n```\n\n### DD_TRACE_ENABLED\n\nInitialize the Datadog tracer when set to `true`. Defaults to `false`.\n\n### DD_MERGE_XRAY_TRACES\n\nSet to `true` to merge the X-Ray trace and the Datadog trace, when using both the X-Ray and Datadog tracing. Defaults to `false`.\n\n### DD_TRACE_MANAGED_SERVICES (experimental)\n\nInferred Spans are spans that Datadog can create based on incoming event metadata.\nSet `DD_TRACE_MANAGED_SERVICES` to `true` to infer spans based on Lambda events.\nInferring upstream spans is only supported if you are using the [Datadog Lambda Extension](https://docs.datadoghq.com/serverless/libraries_integrations/extension/).\nDefaults to `true`.\nInfers spans for:\n\n- API Gateway REST events\n- API Gateway WebSocket events\n- HTTP API events\n- SQS\n- SNS (SNS messaged delivered via SQS are also supported)\n- Kinesis Streams (if data is a JSON string or base64 encoded JSON string)\n- EventBridge (custom events, where Details is a JSON string)\n- S3\n- DynamoDB\n\n### DD_FLUSH_TO_LOG (Deprecated)\n\nWhen the [Datadog Forwarder](https://github.com/DataDog/datadog-serverless-functions/tree/main/aws/logs_monitoring) was launched previously, `DD_FLUSH_TO_LOG` was introduced to control whether to send custom metrics synchronously from your own Lambda function directly to Datadog with added latency (set `DD_FLUSH_TO_LOG` to `false` and you also need to set `DD_API_KEY` and `DD_SITE`) or asynchronously through CloudWatch logs (set `DD_FLUSH_TO_LOG` to `true`).\n\nNow you should consider adopting the [Datadog Lambda Extension](https://docs.datadoghq.com/serverless/libraries_integrations/extension/) for sending custom metrics. When the Datadog Lambda Extension is installed and detected, `DD_FLUSH_TO_LOG` is ignored. If you wish to Defaults to `false`. If set to `false`, you also need to set `DD_API_KEY` and `DD_SITE`.\n\n## Opening Issues\n\nIf you encounter a bug with this package, we want to hear about it. Before opening a new issue, search the existing issues to avoid duplicates.\n\nWhen opening an issue, include the Datadog Lambda Library version, Python version, and stack trace if available. In addition, include the steps to reproduce when appropriate.\n\nYou can also open an issue for a feature request.\n\n## Contributing\n\nIf you find an issue with this package and have a fix, please feel free to open a pull request following the [procedures](CONTRIBUTING.md).\n\n## Community\n\nFor product feedback and questions, join the `#serverless` channel in the [Datadog community on Slack](https://chat.datadoghq.com/).\n\n## License\n\nUnless explicitly stated otherwise all files in this repository are licensed under the Apache License Version 2.0.\n\nThis product includes software developed at Datadog (https://www.datadoghq.com/). Copyright 2019 Datadog, Inc.\n",
    'author': 'Datadog, Inc.',
    'author_email': 'dev@datadoghq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/DataDog/datadog-lambda-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6.0,<4',
}


setup(**setup_kwargs)
