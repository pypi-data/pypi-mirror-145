mod dp_module;

#[cfg(feature = "python")]
mod py_module;

pub use self::dp_module::*;

#[cfg(feature = "wasm")]
use wasm_bindgen::prelude::*;

#[cfg(feature = "wasm")]
#[wasm_bindgen]
pub fn wasm_find_subset(
    keys: String,
    targets: String,
    max_key_length: usize,
    max_target_length: usize,
    n_candidates: usize,
) -> String {
    let mut keys: Vec<i32> = keys
        .split(",")
        .map(|x| x.trim().parse::<i32>().unwrap())
        .collect();
    if targets.contains(",") {
        let mut targets: Vec<i32> = targets
            .split(",")
            .map(|x| x.trim().parse::<i32>().unwrap())
            .collect();
        // if keys.iter().sum::<i32>() != targets.iter().sum::<i32>() {
        //     let ks = keys.iter().sum::<i32>();
        //     let ts = targets.iter().sum::<i32>();
        //     return format!("The sums of two arrays must be the same values. key's sum is {}. target's sum is {}.", ks, ts);
        // }
        // let result: Vec<Vec<(Vec<i32>, Vec<i32>)>> = dp::sequence_matcher(
        //     &mut keys,
        //     &mut targets,
        //     max_key_length,
        //     max_target_length,
        //     n_candidates,
        // ).unwrap();
        let result: Vec<Vec<(Vec<i32>, Vec<i32>)>> = match dp::sequence_matcher(
            &mut keys,
            &mut targets,
            max_key_length,
            max_target_length,
            n_candidates,
        ){
            Ok(res) => res,
            Err(err) => return err,
        };
        if result.len() == 0 {
            return "No solution. You might want to increase maximum length.".to_string();
        }
        dp::sequence_matcher_formatter(result)
    } else {
        let res: Vec<Vec<i32>> =
            dp::find_subset(keys, targets.parse::<i32>().unwrap(), max_target_length);
        let mut r3: Vec<String> = vec![];
        if res.len() == 0 {
            return "No solution. You might want to increase maximum subset length.".to_string();
        }
        for r in res {
            let mut r2: String = r
                .into_iter()
                .map(|x| format!("{}, ", x.to_string()))
                .collect::<String>();
            r2 = format!("[{}]", r2).replace(", ]", "]");
            r3.push(r2);
        }
        let s: String = r3.join(", ");
        s
    }
}
