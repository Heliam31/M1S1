let print s = print_string s
let rec exists p n = if n<0 then 0 else if p n then 1 else exists p (n-1)
let rec divmod a b c= if a < b then (c, a) else divmod (a-b) b (c+1)
let rec make n = if n=0 then [] else [n-1] @ make(n-1)
let rec sum l =
match l with
| [] -> 0
| h::t -> h + (sum t)

let rec makerev n = if n=0 then [] else makerev(n-1) @ [n-1]
let rec map f l =
match l with
| [] -> []
| h::t -> (f h)::(map f t)

let rec fold f i l = 
match l with 
| [] -> i
| h::t -> (f h (fold f i t))