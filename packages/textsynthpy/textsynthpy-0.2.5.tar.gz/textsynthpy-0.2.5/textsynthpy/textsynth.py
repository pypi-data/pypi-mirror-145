from requests import post
from json import loads
from .answer import Complete, Log

class TextSynth():
	"""
	An connector for textsynth.com
	
	:param key: Textsynth API key. You need textsynth.com account to get this.
	:type key: str
	
	:param engine: Textsynth engine to use. It is optional parameter, in default uses "gptj_6B". Aviable engines are on 'https://textsynth.com/documentation.html'
	:param engine: str
	"""
	def __init__(self, key: str, engine = None):
		self.key = key
		if isinstance(engine, str):
			self.engine = engine
		else:
			self.engine = "gptj_6B"
		self.answer = {}
		print(f"Chosen engine: {self.engine}")
	
	def _check(self, max_tokens):
		if self.engine == "gptj_6B":
			max = 2048
		else:
			max = 1024
		if max_tokens > max:
			raise ValueError(f"max_tokens can't be higher than {max} for used engine")
	
	def text_complete(
		self,
		prompt: str,
		max_tokens: int = 100,
		temperature: float = 1,
		top_k: int = 40,
		top_p: float = 0.9,
		stream: bool = False,
		stop: str = None,
		logit_bias: dict = {},
		presence_penalty: int = 0,
		frequency_penalty: int = 0
	):
		"""
		Returns Complete object of completed text by given prompt.
		
		:param prompt: The input text to complete.
		:type prompt: str
		
		:param max_tokens: Optional (Default = 100). Maximum number of tokens to generate. A token represents about 4 characters for English texts. The total number of tokens (prompt + generated text) cannot exceed the model's maximum context length. It is of 2048 for GPT-J and 1024 for the other models. If the prompt length is larger than the model's maximum context length, the beginning of the prompt is discarded.
		:type max_tokens: int
		
		:param temperature: Optional (Default = 1). Sampling temperature. A higher temperature means the model will select less common tokens leading to a larger diversity but potentially less relevant output. It is usually better to tune top_p or top_k.
		:type temperature: int
		
		:param top_k: optional (Range: 1 to 1000, Default = 40). Select the next output token among the top_k most likely ones. A higher top_k gives more diversity but a potentially less relevant output.
		:type top_k: int
		
		:param top_p: optional (Range: 0 to 1, Default = 0.9). Select the next output token among the most probable ones so that their cumulative probability is larger than top_p. A higher top_p gives more diversity, but a potentially less relevant output.
		:type top_p: float
		
		:param stream: Optional (Default = false). If true, the output is streamed so that it is possible to display the result before the complete output is generated. Several JSON answers are output, wrapper returns list of Complete objects
		:type stream: bool
		
		:param stop: (Default = None). Stop the generation when the string(s) are encountered. The generated text does not contain the string. stream must be set to false when this feature is used. The length of the array is at most 5.
		:type stop: str
		
		:param logit_bias: Optional (Default = {}). Modify the likelihood of the specified tokens in the completion. The specified object is a map between the token indexes and the corresponding logit bias. A negative bias reduces the likelihood of the corresponding token. The bias must be between -100 and 100. Note that the token indexes are specific to the selected model. You can use the tokenize api endpoint (tokenize() method) to retrieve the token indexes of a given model. 
Example: if you want to ban the " unicorn" token for GPT-J, you can use: { "44986": -100 }
		:type logit_bias: dict
		
		:param presence_penalty: Optional(Range: -2 to 2, Default = 0). A positive value penalizes tokens which already appeared in the generated text. Hence it forces the model to have a more diverse output.
		:type presence_penalty: int
	
		:param frequency_penalty: Optional number (Range: -2 to 2, Default = 0)
A positive value penalizes tokens which already appeared in the generated text proportionaly to their frequency. Hence it forces the model to have a more diverse output.
		:type frequency_penalty: int
		"""
		self._check(max_tokens)
		
		data = {"prompt": prompt, "max_tokens": max_tokens, "temperature": temperature, "top_k": top_k, "top_p": top_p, "stream": stream, "stop": stop, "logit_bias": logit_bias, "presence_penalty": presence_penalty, "frequency_penalty": frequency_penalty}
		headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.key}"}
	
		answer = (post(f"https://api.textsynth.com/v1/engines/{self.engine}/completions", json = data, headers = headers))
		
		if stream:
			answer = answer.text.split("\n")
			list = []
			for i in answer:
				if i != "":
					print(i)
					temp = loads(i)
					tx = temp.get("text")
					re = temp.get("reached_end")
					inp = temp.get("input_tokens")
					outp = temp.get("output_tokens")
					t = temp.get("truncated_prompt")
					
					b = Complete(text = tx, reached_end = re, truncated_prompt = t, input_tokens = inp, output_tokens = outp)
					list.append(b)
			return list
		else:
			answer = answer.json()
			return Complete(answer["text"], answer["reached_end"], answer["input_tokens"], answer["output_tokens"])
		
	def log_prob(continuation: str = "", context: str = ""):
		"""
		Returns Log object:
		This endpoint returns the logarithm of the probability that a continuation is generated after a context. It can be used to answer questions when only a few answers (such as yes/no) are possible. It can also be used to benchmark the models. 
			
		:param continuation: Must be a non empty string.
		:type continuation: str
			
		:param context: If empty string, the context is set to the End-Of-Text token.
		:type context: str
		"""
		
		if continuation == "":
			raise ValueError("continuation parameter cannot be empty")
			
		data = {"context": context, "continuation": continuation}
		headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.key}"}
		answer = (post(f"https://api.textsynth.com/v1/engines/{self.engine}/logprob", json = data, headers = headers)).json()
		return Log(answer["logprob"], answer["is_greedy"], answer["input_tokens"])
		
	def tokenize(self, text):
		"""
		Method returns array of integers. This endpoint returns the token indexes corresponding to a given text. It is useful for example to know the exact number of tokens of a text or to specify logit biases with the completion endpoint. The tokens are specific to a given model. Note: using tokenize endpoint is free.
		 
		:param text: string
		:type text: str
		"""
		data ={"text": text}
		headers = {"Content-Type": "application/json", "Authorization": f"Bearer {self.key}"}
		return (post(f"https://api.textsynth.com/v1/engines/{self.engine}/tokenize", json = data, headers = headers)).json()["tokens"]