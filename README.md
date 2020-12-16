# testAssignment
a service that:
- Accepts a sequence of HTTP 1.1 messages and their responses via standard input;
  The input is ordered as:  Req_1, Req_2, Req_3, Res_1, Req_4, Res_2, Res_3, Req_5, ... EOF
  (i.e. requests/responses are ordered among themselves; but can intermix such that requests are delayed)
- Each input record ends with CR-LF, a line with 80 "-", and another CR-LF
- For each Req it prints the end-point, the method, and the arguments;
- For each Res it prints the payload, decoded if applicable (at least in case of json)
