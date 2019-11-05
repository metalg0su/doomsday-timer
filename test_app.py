from main import parse_data, TermData, make_result
import datetime

response_result = {
    'jsonrpc': '2.0',
    'result': {
        'blockHeight': '0xa2b2f7',
        'variable': {
            'irep': '0xa968163f0a57b400000',
            'rrep': '0x2ab'
        },
        'nextCalculation': '0xa2b7f3',
        'nextPRepTerm': '0xa2b7f3',
        'rcResult': {
            'iscore': '0xa440fa4ca50f0a12fc8889',
            'estimatedICX': '0x2a0c89cdfd32f43e345c',
            'startBlockHeight': '0xa16713',
            'endBlockHeight': '0xa20f82'
        }
    },
    'id': 1
}


class Test:
    def test_parse_response_parses_well(self):
        parsed_data: TermData = parse_data(response_result)

        assert isinstance(parsed_data, TermData)
        assert isinstance(parsed_data.current_height, int)
        assert isinstance(parsed_data.target_height, int)
        assert isinstance(parsed_data.height_left, int)

        assert isinstance(parsed_data.current_datetime, datetime.datetime)
        assert isinstance(parsed_data.est_datetime, datetime.datetime)

        assert isinstance(parsed_data.hours_left, int)
        assert isinstance(parsed_data.minutes_left, int)
        assert isinstance(parsed_data.seconds_left, int)

    def test_result(self):
        parsed_data: TermData = parse_data(response_result)
        assert make_result(parsed_data)

